from typing import Any, Optional, Union
from fates import tables, models
from ruamel.yaml import YAML
import orjson
import bleach
import cmarkgfm
import msgpack
import aiohttp
from cmarkgfm.cmark import Options as cmarkgfmOptions
from maplecache import *


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

class Permission:
    def __init__(self, index: int, roles: list[int], name: str):
        self.index = index
        self.roles = roles
        self.name = name
    
    def __eq__(self, other: "Permission") -> bool:
        if not isinstance(other, Permission):
            return False
        return self.index == other.index
    
    def __lt__(self, other: "Permission") -> bool:
        if not isinstance(other, Permission):
            return False
        return self.index < other.index
    
    def __gt__(self, other: "Permission") -> bool:
        if not isinstance(other, Permission):
            return False
        return self.index > other.index

class Mapleshade:
    __slots__ = [
        "yaml",
        "config",
        "sanitize_tags",
        "sanitize_attrs",
        "cache",
        "cmark_opts",
        "cmark_exts",
        "perms"
    ]

    def __init__(self):
        # In memory cache for bot data
        self.cache = Cache()

        self.yaml = YAML()

        with open("config.yaml") as doc:
            self.config = self.yaml.load(doc)
        
        self.perms = {
            "default": Permission(0, [], "default"),
        }

        for name, perm in self.config["perms"].items():
            self.perms[name] = Permission(
                index=perm["index"],
                roles=perm["roles"],
                name=name
            )

        # CMark options
        self.cmark_opts = (
            # cmarkgfmOptions.CMARK_OPT_LIBERAL_HTML_TAG |
            cmarkgfmOptions.CMARK_OPT_UNSAFE
            | cmarkgfmOptions.CMARK_OPT_SMART
        )

        self.cmark_exts = ("table", "autolink", "strikethrough", "tasklist")

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
    
    async def guppy(self, user_id: int) -> Permission:
        """Guppy: (Get User Permissions Pretty Please You!"""
        try:
            user_roles: list[int] = await self.silverpelt_req(f"roles/{self.config['main_server']}/{user_id}")
        except SilverNoData:
            return self.perms["default"]
        
        for perm in self.perms.values():
            if any(role in user_roles for role in perm.roles):
                return perm
        
        return self.perms["default"]

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
        long_description_type: models.LongDescriptionType = models.LongDescriptionType.MarkdownServerSide,
    ) -> str:
        """Sanitize a string for use in HTML/MD accordingly"""
        if long_description_type == models.LongDescriptionType.MarkdownServerSide:
            # First parse markdown
            s = cmarkgfm.markdown_to_html_with_extensions(
                s, options=self.cmark_opts, extensions=self.cmark_exts
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
            "<style>" + (bot["css"] or "") + "</style>", models.LongDescriptionType.Html
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
        if bot["features"]:
            for feature in bot["features"]:
                feature_data = (
                    await tables.Features.select()
                    .where(tables.Features.id == feature)
                    .first()
                )
                features.append(feature_data)

            bot["features"] = models.Feature.to_list(features)
        else:
            bot["features"] = []

        bot["commands"] = await tables.BotCommands.select().where(
            tables.BotCommands.bot_id == bot_id
        )

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
                    entity["user"] = await self.silverpelt_req(
                        f"users/{entity['bot_id']}"
                    )
                except:
                    print(f"Failed to get user for bot {entity['bot_id']}")
                    continue
            snippet.append(models.Snippet(**entity))

        return snippet
