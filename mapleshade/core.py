import time
from typing import Any, Optional
from fates import tables, models, enums
from ruamel.yaml import YAML
import orjson
import bleach
import cmarkgfm
import msgpack
import aiohttp
import asyncio
from cmarkgfm.cmark import Options as cmarkgfmOptions


class SilverException(Exception):
    """Base exception for Silverpelt"""
    ...

class SilverRespError(SilverException):
    """Exception for when a response is not okay (200)"""

    def __init__(self, endpoint: str, kwargs: dict, resp: aiohttp.ClientResponse):
        self.resp = resp
        self.endpoint = endpoint
        self.kwargs = kwargs
        super().__init__(
            f"Silverpelt returned {resp.status} on {endpoint} with kwargs {kwargs}"
        )


class SilverNoData(SilverException):
    """Exception for when there is no data"""

    ...

class CacheValue():
    """Mapleshade cache value"""
    def __init__(self, parent: "Cache", key: str, value: Any, *, expiry: int | float):
        self._val = value
        self.parent = parent
        self.key = key
        self.expiry = expiry

        # Start task to clear from cache when expired
        if expiry:
            self.cleanup = asyncio.create_task(self._clear_cache())

    async def _clear_cache(self):
        """Clears the cache"""
        expiry = self.expiry - time.time()
        await asyncio.sleep(expiry)
        self.parent.remove(self.key)
        self._val = None # Clear value
        return
            
    def expired(self):
        if not self.expiry:
            return False
        return self.expiry < time.time()
    
    def borrow(self) -> "BorrowedCacheValue":
        return BorrowedCacheValue(
            self.key,
            self._val,
            expiry=self.expiry,
        )
    
    def remove(self):
        """Removes this cache"""
        self._val = None
        self.cleanup.cancel()
        self.expiry = 0
    
    def edit(self, value: Any, *, expiry: Optional[int | float] = None):
        """Edit the value and expiry"""
        self._val = value
        if expiry:
            self.expiry = expiry
            self.cleanup.cancel()
        self.cleanup = asyncio.create_task(self._clear_cache())

class BorrowedCacheValue():
    """Mapleshade Cache value (borrowed from cache)"""
    __slots__ = ("_init", "_val", "key", "expiry", "empty")
    def __init__(self, key: str, value: Any, *, expiry: int | float):
        self._init = True
        self._val = value
        self.key = key
        self.expiry = expiry
        self.empty = self._val is None

        self._init = False

    def __repr__(self):
        return f"<CacheValue value={self._val} expiry={self.expiry} empty={self.empty}>"

    def __str__(self):
        return self.__repr__()
    
    def value(self):
        return self._val
    
    def expired(self):
        if not self.expiry:
            return False
        return self.expiry < time.time()
    
    def __delattr__(self, __name: str) -> None:
        raise AttributeError("Cannot delete attributes on borrowed cache value")

    def __setattr__(self, name: str, value: Any):
        if getattr(self, "_init", True):
            return super().__setattr__(name, value)
        raise AttributeError("Cannot set attributes on borrowed cache value")

class Cache():
    """Cache for Mapleshade with expiry"""

    __slots__ = ["cache"]

    def __init__(self):
        self.cache: dict[str, CacheValue] = {}

        # Start task to clear cache
        asyncio.create_task(self._clear_cache())
    
    def remove(self, key: str) -> bool:
        """Deletes a value from the cache"""
        try:
            del self.cache[key]
            return True
        except:
            return False
    
    async def _clear_cache(self):
        """Clears the cache"""
        while True:
            to_remove = []
            for key in self.cache:
                if self.cache[key].expired():
                    to_remove.append(key)
            
            for key in to_remove:
                self.cache[key].remove()
                self.remove(key)
            await asyncio.sleep(360)
    
    def get(self, key: str) -> Optional[BorrowedCacheValue]:
        """Gets a snippet from the cache"""
        if key in self.cache:
            cached_data = self.cache[key]
            if cached_data.expired():
                self.remove(key)
                return None
            return cached_data.borrow()
        return None
    
    def set(self, key: str, value: Any, *, expiry: Optional[int | float] = None, **kwargs) -> Any:
        """Sets a value in the cache"""
        if isinstance(value, CacheValue):
            raise TypeError("Value must not be of type CacheValue")

        if key in self.cache:
            self.cache[key].edit(value, expiry=expiry)

        self.cache[key] = CacheValue(
            self,
            key,
            value,
            expiry=(time.time() + expiry) if expiry else None,
            **kwargs
        )

class BackendDoc:
    def __init__(self, fn: str):
        try:
            with open(f"backend_assets/{fn}.kitescratch") as doc:
                doc.read()
        except FileNotFoundError:
            raise RuntimeError(f"BackendDoc {fn} not found. Have you run kitescratch/genassets?")

class Mapleshade:
    __slots__ = ["yaml", "config", "sanitize_tags", "sanitize_attrs", "cache", "cmark_opts", "cmark_exts"]

    def __init__(self):
        # In memory cache for bot data
        self.cache = Cache()

        self.yaml = YAML()

        with open("config.yaml") as doc:
            self.config = self.yaml.load(doc)
        
        # CMark options
        self.cmark_opts = (
            #cmarkgfmOptions.CMARK_OPT_LIBERAL_HTML_TAG |
            cmarkgfmOptions.CMARK_OPT_UNSAFE |
            cmarkgfmOptions.CMARK_OPT_SMART
        )

        self.cmark_exts = (
            'table', 'autolink', 'strikethrough', 'tasklist'
        )

        # Sanitize tags for bleach
        self.sanitize_tags = bleach.sanitizer.ALLOWED_TAGS + [
            "span",
            "img",
            "video",
            "iframe",
            "style",
            "p",
            "br",
            "center",
            "div",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "section",
            "article",
            "fl-lang",
        ]

        # Sanitize attributes for bleach
        self.sanitize_attrs = bleach.sanitizer.ALLOWED_ATTRIBUTES | {
            "*": [
                "id",
                "class",
                "style",
                "data-src",
                "data-background-image",
                "data-background-image-set",
                "data-background-delimiter",
                "data-icon",
                "data-inline",
                "data-height",
                "code",
            ],
            "iframe": ["src", "height", "width"],
            "img": [
                "src",
                "alt",
                "width",
                "height",
                "crossorigin",
                "referrerpolicy",
                "sizes",
                "srcset",
            ],
        }

    def load_doc(self, fn: str) -> str:
        cached_text = self.cache.get(f"doc:{fn}")
        if cached_text:
            return cached_text.value()
        try:
            with open(f"backend_assets/{fn}.kitescratch") as doc:
                f = cmarkgfm.markdown_to_html_with_extensions(doc.read(), options=self.cmark_opts, extensions=self.cmark_exts)
                self.cache.set(f"doc:{fn}", f, expiry=60)
                return f
        except FileNotFoundError:
            raise RuntimeError(f"BackendDoc {fn} not found. Have you run kitescratch/genassets?")


    def parse_dict(self, d: dict | object) -> dict | object:
        """Parse dict for handling bigints in DDR's etc"""
        if isinstance(d, int):
            if d > 9007199254740991:
                return str(d)
            return d
        elif isinstance(d, list):
            return [self.parse_dict(i) for i in d]
        elif isinstance(d, dict):
            nd = {}  # New dict
            for k, v in d.items():
                nd[k] = self.parse_dict(v)
            return nd
        else:
            return d

    def sanitize(
        self,
        s: str,
        long_description_type: enums.LongDescriptionType = enums.LongDescriptionType.MarkdownServerSide,
    ) -> str:
        """Sanitize a string for use in HTML/MD accordingly"""
        if long_description_type == enums.LongDescriptionType.MarkdownServerSide:
            # First parse markdown
            s = cmarkgfm.markdown_to_html_with_extensions(
                s,
                options=self.cmark_opts,
                extensions=self.cmark_exts
            )
        return bleach.clean(
            s,
            tags=self.sanitize_tags,
            attributes=self.sanitize_attrs,
        )

    async def bot(self, bot_id: int) -> Optional[models.Bot]:
        """Returns a bot from the database"""
        bot = await tables.Bots.select().where(tables.Bots.bot_id == bot_id).first()

        if not bot:
            return None

        # Get bot user
        try:
            bot["user"] = await self.silverpelt_req(f"users/{bot_id}")
        except SilverNoData:
            return None

        owners = await tables.BotOwner.select(
            tables.BotOwner.owner, tables.BotOwner.main
        ).where(tables.BotOwner.bot_id == bot_id)

        owners_list: list = []

        for owner in owners:
            try:
                owner_user = await self.silverpelt_req(f"users/{owner['owner']}")
            except SilverNoData:
                continue

            owners_list.append(models.Owner(user=owner_user, main=owner["main"]))

        bot["owners"] = owners_list

        # Add action logs
        bot["action_logs"] = (
            await tables.UserBotLogs.select().where(tables.UserBotLogs.bot_id == bot_id)
        ) or []

        # Fix extra_links not being a dict (despite being JSONB, this is just stupid)
        bot["extra_links"] = orjson.loads(bot["extra_links"])

        # Sanitize long description
        bot["long_description_raw"] = bot["long_description"]
        bot["long_description"] = self.sanitize(bot["long_description"])

        # Sanitize CSS
        bot["css_raw"] = bot["css"]
        bot["css"] = self.sanitize(
            "<style>" + (bot["css"] or "") + "</style>", enums.LongDescriptionType.Html
        )

        # Tags
        tags = []
        bot_tags = await tables.BotTags.select(tables.BotTags.tag).where(
            tables.BotTags.bot_id == bot_id
        )

        for tag in bot_tags:
            tag_data = (
                await tables.BotListTags.select()
                .where(tables.BotListTags.id == tag["tag"])
                .first()
            )
            tags.append(tag_data)

        bot["tags"] = models.Tag.to_list(tags)

        # Features
        features = []
        for feature in bot["features"]:
            feature_data = (
                await tables.Features.select()
                .where(tables.Features.id == feature)
                .first()
            )
            features.append(feature_data)

        bot["features"] = models.Feature.to_list(features)

        # Pydantic memes
        bot_m = models.Bot(**bot)

        return bot_m

    async def user(self, user_id: int) -> Optional[models.User]:
        """Returns a user from the database"""
        user = (
            await tables.Users.select().where(tables.Users.user_id == user_id).first()
        )

        if not user:
            return None

        return models.User(**user)

    async def silverpelt_req(self, endpoint: str, **kwargs) -> dict:
        """Makes a request to Silverpelt"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"http://127.0.0.1:3030/{endpoint}", **kwargs
                ) as resp:
                    if not resp.ok:
                        raise SilverRespError(endpoint, kwargs, resp)
                    body_bytes = await resp.read()
                    bytes: dict = msgpack.unpackb(body_bytes)

                    if not bytes:
                        raise SilverNoData(
                            f"Silverpelt returned no data on {endpoint} with kwargs {kwargs}"
                        )

                    return bytes
            except aiohttp.ClientConnectorError:
                raise SilverException("Could not connect to Silverpelt")

    async def to_snippet(self, data: list[dict]) -> models.Snippet:
        """Converts a dict to a snippet"""
        snippet = []
        for entity in data:
            if entity.get("bot_id"):
                # This is a bot
                try:
                    entity["user"] = await self.silverpelt_req(f"users/{entity['bot_id']}")
                except:
                    print(f"Failed to get user for bot {entity['bot_id']}")
                    continue
            snippet.append(models.Snippet(**entity))
        
        return snippet