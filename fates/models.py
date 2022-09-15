from typing import Literal, Optional
from typing_extensions import Self

from fates import enums
from .tables import Bots, Users, UserBotLogs
from piccolo.utils.pydantic import create_pydantic_model
from piccolo.query import Select
from pydantic import BaseModel
import silverpelt.types.types as silver_types

from fates import tables

# Add models here
BotBase = create_pydantic_model(
    Bots,
    deserialize_json=True,
    exclude_columns=(
        Bots.api_token,
        Bots.webhook_secret,
        Bots.webhook,
    ),
)
UserBase = create_pydantic_model(
    Users, deserialize_json=True, exclude_columns=(Users.api_token,)
)

UserBotLogsBase = create_pydantic_model(UserBotLogs, deserialize_json=True)

BOT_SNIPPET_COLS = (
    Bots.bot_id,
    Bots.votes,
    Bots.description,
    Bots.flags,
    Bots.guild_count,
    Bots.banner_card,
    Bots.state,
)

async def augment(c: Select, aug: str):
    """Augment a SQL select with custom SQL"""
    return await tables.Bots.raw(str(c) + aug)

# kitescratch-begin

class UserBotLog(UserBotLogsBase):  # type: ignore[valid-type, misc]
    bot_id: str
    user_id: str

    # kitescratch-end


class Entity:
    """Base class for all entities"""

    id: str
    """The entity's ID"""

    # kitescratch-end

    @staticmethod
    def to(_: dict) -> "Entity":
        pass

    @classmethod
    def to_list(cls, obj: list[dict]) -> list["Entity"]:
        return [cls.to(e) for e in obj]

    def __eq__(self, other):
        if getattr(other, "id", None):
            return self.id == getattr(other, "id", None)
        return self.id == other


class Tag(BaseModel, Entity):
    """Represents a tag"""

    id: str
    """The tag's ID"""

    iconify_data: str
    """The tag's iconify class"""

    name: str
    """The tag name"""

    owner_guild: Optional[str]
    """The guild ID of the tags owner (server only)"""

    # kitescratch-end

    @staticmethod
    def to(tag: dict) -> "Tag":
        """Returns all tags for a bot"""
        return Tag(
            id=tag["id"],
            iconify_data=tag["icon"] if "icon" in tag else tag["iconify_data"],
            name=tag["id"].replace("_", "").title(),
            owner_guild=tag.get("owner_guild", None),
        )


class Feature(BaseModel, Entity):
    """Represents a feature"""

    id: str
    """The feature's ID"""

    name: str
    """Feature Name"""

    viewed_as: str
    """What the feature is viewed as"""

    description: str
    """Feature description"""

    # kitescratch-end

    @staticmethod
    def to(feature: dict) -> "Feature":
        """Returns all features for a bot"""
        return Feature(
            id=feature["id"],
            name=feature["name"],
            viewed_as=feature["viewed_as"],
            description=feature["description"],
        )


class Owner(BaseModel):
    """Represents a bot owner"""

    user: silver_types.DiscordUser
    """The owner's user object"""

    main: bool
    """Whether the owner is the main owner"""

    # kitescratch-end


class Bot(BotBase):  # type: ignore[misc, valid-type]
    """Represents a bot"""

    user: silver_types.DiscordUser
    """The bot's user object"""

    owners: list[Owner]
    """The bot's owners"""

    # These fields have the wrong type set for API response, change them
    bot_id: str

    verifier: Optional[str]
    """The reviewer who has approved/denied the bot"""

    extra_links: dict
    """Extra links for the bot ({"Website": "https://blah.com"})"""

    long_description_raw: str
    """Raw unsanitized long description"""

    css_raw: str
    """Raw unsanitized CSS"""

    action_logs: list[UserBotLog]
    """Action logs for the bot"""

    tags: list[Tag]
    """Tags for the bot"""

    features: list[Feature]
    """Features for the bot"""

    state: enums.BotServerState
    """The bot's state"""

    flags: list[enums.BotServerFlag]
    """The bot's flags"""

    # kitescratch-end

class User(UserBase):  # type: ignore[valid-type, misc]
    """Represents a user"""
    pass

class Snippet(BaseModel):
    """
Represents a snippet which is essentially a miniature version of a bot/server where a full Bot is too expensive to return

- This applies to both ``Bot`` and ``Server`` entities

    """
    user: silver_types.DiscordUser
    """The bot's/server's user object"""

    votes: int
    """The bot's/server's vote count"""

    description: str
    """The bot's/server's short description"""

    flags: list[enums.BotServerFlag]
    """The bot's/server's flags"""

    banner_card: Optional[str]
    """The bot's/server's banner_card"""

    state: enums.BotServerState
    """The bot's/server's state"""

    guild_count: int
    """The bot's/server's guild count"""

    # kitescratch-end

class Index(BaseModel):
    """Represents an index"""

    new: list[Snippet]
    """New bots/servers"""

    top_voted: list[Snippet]
    """Top voted bots/servers"""

    certified: list[Snippet]
    """Certified bots/servers this week"""

    # kitescratch-end

class BotListMeta(BaseModel):
    """Core metadata about the bot list part of fates list"""

    tags: list[Tag]
    """All tags for a bot"""

    features: list[Feature]
    """All features for a bot"""

class ServerListMeta(BaseModel):
    """Core metadata about the server list part of fates list"""
    
    tags: list[Tag]
    """All tags for a server"""

class ListMeta(BaseModel):
    """Core metadata (tags/features for servers and bots)"""

    bot: BotListMeta

    server: ServerListMeta

    # kitescratch-end