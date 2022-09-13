from typing import Optional
from fates import tables, models, enums
from ruamel.yaml import YAML
import orjson
import bleach
import cmarkgfm
import msgpack
import aiohttp

class SilverException(Exception):
    """Base exception for Silverpelt"""
    ...

class SilverRespError(SilverException):
    """Exception for when a response is not okay (200)"""
    def __init__(self, endpoint: str, kwargs: dict, resp: aiohttp.ClientResponse):
        self.resp = resp
        self.endpoint = endpoint
        self.kwargs = kwargs
        super().__init__(f"Silverpelt returned {resp.status} on {endpoint} with kwargs {kwargs}")

class SilverNoData(SilverException):
    """Exception for when there is no data"""
    ...

class Mapleshade():
    __slots__=['yaml', 'config', 'sanitize_tags', 'sanitize_attrs']
    def __init__(self):
        self.yaml = YAML()

        with open("config.yaml") as doc:
            self.config = self.yaml.load(doc)

        # Sanitize tags for bleach
        self.sanitize_tags = bleach.sanitizer.ALLOWED_TAGS + [
            "span", "img", "video", "iframe", "style", "p", "br", "center", "div", "h1", "h2",
            "h3", "h4", "h5", "section", "article", "fl-lang",
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
            "iframe": [
                "src", 
                "height", 
                "width"
            ],
            "img": [
                "src",
                "alt",
                "width",
                "height",
                "crossorigin",
                "referrerpolicy",
                "sizes",
                "srcset",
            ]
        }


    def parse_dict(self, d: dict | object) -> dict | object:
        """Parse dict for handling bigints in DDR's etc"""
        if isinstance(d, int):
            if d > 9007199254740991:
                return str(d)
            return d
        elif isinstance(d, list):
            return [self.parse_dict(i) for i in d]
        elif isinstance(d, dict):
            nd = {} # New dict
            for k, v in d.items():
                nd[k] = self.parse_dict(v)
            return nd
        else:
            return d
    
    def sanitize(
        self, 
        s: str, 
        long_description_type: enums.LongDescriptionType = enums.LongDescriptionType.MarkdownServerSide
    ) -> str:
        """Sanitize a string for use in HTML/MD accordingly"""
        if long_description_type == enums.LongDescriptionType.MarkdownServerSide:
            # First parse markdown
            s = cmarkgfm.github_flavored_markdown_to_html(s)
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
        
        # Add action logs
        bot["action_logs"] = (await tables.UserBotLogs.select().where(tables.UserBotLogs.bot_id == bot_id)) or []
        
        # Fix extra_links not being a dict (despite being JSONB, this is just stupid)
        bot["extra_links"] = orjson.loads(bot["extra_links"])

        # Sanitize long description
        bot['long_description_raw'] = bot['long_description']
        bot['long_description'] = self.sanitize(bot['long_description'])

        # Sanitize CSS
        bot["css_raw"] = bot["css"]
        bot['css'] = self.sanitize("<style>" + (bot['css'] or "") + "</style>", enums.LongDescriptionType.Html)

        # Tags
        tags = []
        bot_tags = await tables.BotTags.select(tables.BotTags.tag).where(tables.BotTags.bot_id == bot_id)

        for tag in bot_tags:
            tag_data = await tables.BotListTags.select().where(tables.BotListTags.id == tag["tag"]).first()
            tags.append(tag_data)

        bot["tags"] = models.Tag.to_list(tags)
        
        # Pydantic memes
        bot_m = models.Bot(**bot)

        return bot_m
    
    async def user(self, user_id: int) -> Optional[models.User]:
        """Returns a user from the database"""
        user = await tables.Users.select().where(tables.Users.user_id == user_id).first()

        if not user:
            return None

        return models.User(**user)
    
    async def silverpelt_req(self, endpoint: str, **kwargs) -> dict:
        """Makes a request to Silverpelt"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"http://127.0.0.1:3030/{endpoint}", **kwargs) as resp:
                    if not resp.ok:
                        raise SilverRespError(endpoint, kwargs, resp)
                    body_bytes = await resp.read()
                    bytes: dict = msgpack.unpackb(body_bytes)

                    if not bytes:
                        raise SilverNoData(f"Silverpelt returned no data on {endpoint} with kwargs {kwargs}")
                    
                    return bytes
            except aiohttp.ClientConnectorError:
                raise SilverException("Could not connect to Silverpelt")