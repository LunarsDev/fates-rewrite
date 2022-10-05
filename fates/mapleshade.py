"""The Mapleshade class contains a set of common primitives for the Fates List backend"""
from datetime import datetime
import random
import string
from typing import Any, Optional
from fates import tables, models
from ruamel.yaml import YAML
import orjson
import bleach
import cmarkgfm
import msgpack
import aiohttp
from cmarkgfm.cmark import Options as cmarkgfmOptions
from maplecache import *
import pytz
import asyncpg


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


class SQLFiles:
    def load_sql(self, fn: str) -> str:
        """Load SQL from a file"""
        with open(f"fates/sql/{fn}.sql") as doc:
            return doc.read()

    def __init__(self):
        self.data_delete_find_bots = self.load_sql("data_delete_find_bots")
        self.data_request_get_tables = self.load_sql("data_request_get_tables")
        self.search_bots = self.load_sql("search_bots")
        self.search_servers = self.load_sql("search_servers")
        self.search_profiles = self.load_sql("search_profiles")
        self.search_packs = self.load_sql("search_packs")


class Mapleshade:
    __slots__ = [
        "yaml",
        "config",
        "sanitize_tags",
        "sanitize_attrs",
        "cache",
        "cmark_opts",
        "cmark_exts",
        "perms",
        "utc",
        "sql",
        "pool",  # Raw SQL pool
    ]

    def __init__(self):
        # In memory cache for bot data
        self.cache = Cache()

        self.yaml = YAML()

        with open("config.yaml") as doc:
            self.config: dict[str, Any] = self.yaml.load(doc)

        self.perms = {
            "default": models.Permission(index=0, roles=[], name="default"),
        }

        for name, perm in self.config["perms"].items():
            self.perms[name] = models.Permission(
                index=perm["index"], roles=perm["roles"], name=name
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

        self.utc = pytz.UTC
        self.sql = SQLFiles()
        self.pool: asyncpg.Pool | None = None  # Initially none

    def compare_dt(self, dt1: datetime, dt2: datetime):
        """Return True if dt1 is greater than dt2. Handles both naive and aware datetimes"""
        return self.utc.localize(dt1.replace(tzinfo=None)) > dt2.replace(
            tzinfo=self.utc
        )

    async def guppy(self, user_id: int) -> models.Permission:
        """Guppy: (Get User Permissions Pretty Please You!"""
        try:
            user_roles: list[str] = [
                str(v)
                for v in await self.silverpelt_req(
                    f"roles/{self.config['main_server']}/{user_id}"
                )
            ]
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

        for tag in bot["tags"]:
            tag_data = (
                await tables.BotListTags.select()
                .where(tables.BotListTags.id == tag)
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
        """Converts a dict to a snippet (bots/servers only). Profiles should use to_profile_snippet"""
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
            elif entity.get("guild_id"):
                # This is a guild
                try:
                    guild_data = (
                        await tables.Servers.select(
                            tables.Servers.name_cached,
                            tables.Servers.avatar_cached,
                        )
                        .where(tables.Servers.guild_id == entity["guild_id"])
                        .first()
                    )

                    entity["user"] = {
                        "id": entity["guild_id"],
                        "username": guild_data["name_cached"],
                        "disc": "0001",
                        "avatar": guild_data["avatar_cached"],
                        "bot": False,
                        "system": False,
                        "status": 0,
                        "flags": 0,
                    }
                except:
                    print(f"Failed to get guild for {entity['guild_id']}")
                    continue
            else:
                raise ValueError("Invalid entity")
            snippet.append(models.Snippet(**entity))

        return snippet

    async def to_profile_snippet(self, data: list[dict]) -> models.ProfileSnippet:
        """Converts a dict to a snippet (profiles only)"""
        snippet = []
        for entity in data:
            try:
                entity["user"] = await self.silverpelt_req(f"users/{entity['user_id']}")
            except:
                print(f"Failed to get user for profile {entity['user_id']}")
                continue
            snippet.append(models.ProfileSnippet(**entity))

        return snippet

    async def resolve_packs(self, data: list[dict]) -> list[models.BotPack]:
        packs = []
        for pack in data:
            resolved_bots = []

            for bot in pack["bots"]:
                description = (
                    await tables.Bots.select(tables.Bots.description)
                    .where(tables.Bots.bot_id == bot)
                    .first()
                )

                if description:
                    try:
                        user = await self.silverpelt_req(f"users/{bot}")
                    except:
                        print(f"Failed to get user for bot {bot}")
                        continue
                    resolved_bots.append(
                        models.ResolvedPackBot(
                            user=user,
                            description=description["description"],
                        )
                    )

            try:
                pack["owner"] = await self.silverpelt_req(f"users/{pack['owner']}")
            except:
                print(f"Failed to get user for pack owner {pack['owner']}")
                continue

            packs.append(models.BotPack(**pack, resolved_bots=resolved_bots))

        return packs

    def gen_secret(self, n: int = 32) -> str:
        """Generates a secret"""
        return bytes(random.choices(string.ascii_letters.encode("ascii"), k=n)).decode(
            "ascii"
        )

    async def login(self, code: str, redirect_url: str) -> models.OauthUser:
        """Logs a user in"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://discord.com/api/v10/oauth2/token",
                data={
                    "client_id": self.config["secrets"]["client_id"],
                    "client_secret": self.config["secrets"]["client_secret"],
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_url,
                },
            ) as resp:
                data = await resp.json()
                if not resp.ok:
                    raise Exception(
                        f"Failed to get token with status code: {resp.status} [err of {data}]"
                    )

            async with session.get(
                "https://discord.com/api/v10/users/@me",
                headers={"Authorization": f"Bearer {data['access_token']}"},
            ) as resp:
                duser = await resp.json()
                if not resp.ok:
                    raise Exception(
                        f"Failed to get user with status code: {resp.status} [err of {duser}]"
                    )

        user = await self.silverpelt_req(
            f"users/{duser['id']}",
        )

        duser["id"] = int(duser["id"])

        list_data = (
            await tables.Users.select(
                tables.Users.state,
                tables.Users.api_token,
                tables.Users.user_css,
                tables.Users.username,
                tables.Users.site_lang,
                tables.Users.experiments,
            )
            .where(tables.Users.user_id == duser["id"])
            .first()
        )

        if not list_data:
            await tables.Users.insert(
                tables.Users(
                    id=duser["id"],
                    user_id=duser["id"],
                    username=duser["username"],
                    user_css="",
                    site_lang="en",
                    api_token=self.gen_secret(128),
                )
            )

            list_data = (
                await tables.Users.select(
                    tables.Users.state,
                    tables.Users.api_token,
                    tables.Users.user_css,
                    tables.Users.username,
                    tables.Users.site_lang,
                    tables.Users.experiments,
                )
                .where(tables.Users.user_id == duser["id"])
                .first()
            )

        return models.OauthUser(
            state=list_data["state"],
            token=list_data["api_token"],
            user=user,
            site_lang=list_data["site_lang"],
            css=list_data["user_css"],
            user_experiments=models.DEFAULT_USER_EXPERIMENTS + list_data["experiments"],
            permissions=await self.guppy(duser["id"]),
        )

    def parse_records(self, records: list) -> list[dict]:
        """Parses a list of records"""
        if records:
            return [dict(record) for record in records]
        else:
            return records

    async def search(
        self,
        query: models.SearchQuery,
    ):
        record_bots = self.parse_records(
            await self.pool.fetch(
                self.sql.search_bots,
                f"%{query.query}%",
                models.BotServerState.Approved,
                models.BotServerState.Certified,
                query.tags.bot,
                *query.guild_count,
                *query.votes,
            )
        )

        bots = await self.to_snippet(record_bots)

        record_servers = self.parse_records(
            await self.pool.fetch(
                self.sql.search_servers,
                f"%{query.query}%",
                models.BotServerState.Approved,
                models.BotServerState.Certified,
                query.tags.server,
                *query.guild_count,
                *query.votes,
            )
        )

        servers = await self.to_snippet(record_servers)

        record_profiles = self.parse_records(
            await self.pool.fetch(
                self.sql.search_profiles,
                f"%{query.query}%",
                models.BotServerState.Approved,
                models.BotServerState.Certified,
            )
        )

        profiles = await self.to_profile_snippet(record_profiles)

        record_packs = self.parse_records(
            await self.pool.fetch(
                self.sql.search_packs,
                f"%{query.query}%",
            )
        )

        packs = await self.resolve_packs(record_packs)

        return models.SearchResponse(
            bots=bots,
            servers=servers,
            profiles=profiles,
            packs=packs,
        )
