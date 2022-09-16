from enum import Enum, IntEnum
from typing import Optional

from .tables import BotCommands, Bots, Users, UserBotLogs
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

BotCommandsBase = create_pydantic_model(BotCommands, deserialize_json=True)

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

class WidgetFormat(Enum):
    """Widget format"""

    json = "json"
    """Raw JSON format"""
    
    html = "html"
    """HTML format"""

    png = "png"
    """PNG image format. May produce better results than WEBP"""

    webp = "webp"
    """WebP image format"""

    # kitescratch-end

class BotServerFlag(IntEnum):
    """Flags that apply to both bots and servers"""

    Unlocked = 0
    """Bot or server is unlocked and can be freely editted"""
    
    EditLocked = 1
    """Bot or server is locked and cannot be editted but can be unlocked by the owner"""

    StaffLocked = 2
    """Bot or server is locked by staff and can only be unlocked by staff"""

    StatsLocked = 3
    """Bot or server stats are locked due to abuse"""
    
    VoteLocked = 4
    """Bot or server is locked from voting due to abuse"""

    System = 5
    """Bot or server is a system bot or server"""

    WhitelistOnly = 6
    """Server is a whitelist only server (it cannot be joined without being whitelisted by staff on said server)"""

    KeepBannerDecor = 7
    """Bot or server banner should keep special fallback banner styles"""

    NSFW = 8
    """Bot or server is NSFW"""

    LoginRequired = 9
    """Server requires the user to be logged in to join"""

    # kitescratch-end

class UserFlag(IntEnum):
    """Flags that apply to users"""

    Unknown = 0
    """Unknown flag"""

    VotesPrivate = 1
    """User's votes are private"""

    Staff = 2
    """User is a *public* staff member"""

    AvidVoter = 3
    """User is an avid voter"""

    # kitescratch-end

class UserState(IntEnum):
    """User states"""

    Normal = 0
    """User is normal (no bans)"""

    GlobalBan = 1
    """User is globally banned from the list"""

    ProfileEditBan = 2
    """User is banned from editing their profile due to abuse"""

    # kitescratch-end

class BotServerState(IntEnum):
    Approved = 0
    Pending = 1
    Denied = 2
    Hidden = 3
    Banned = 4
    UnderReview = 5
    Certified = 6
    Archived = 7
    PrivateViewable = 8
    PrivateStaffOnly = 9


class EventType(IntEnum):
    promotion = 0
    maintenance = 1
    announcement = 2


class Vanity(IntEnum):
    server = 0
    bot = 1


class UserBotAction(IntEnum):
    approve = 0
    deny = 1
    certify = 2
    ban = 3
    claim = 4
    unclaim = 5
    transfer_ownership = 6
    edit_bot = 7
    delete_bot = 8
    unban = 9
    uncertify = 10
    unverify = 11
    requeue = 12


class LongDescriptionType(IntEnum):
    Html = 0
    MarkdownServerSide = 1


class WebhookType(IntEnum):
    vote = 0
    discord = 1


class CommandType(IntEnum):
    regular = 0
    guild_slash = 1
    global_slash = 2


class TargetType(IntEnum):
    Bot = 0
    Server = 1


class PageStyle(IntEnum):
    tabs = 0
    single_scroll = 1
    

class UserBotLog(UserBotLogsBase):  # type: ignore[valid-type, misc]
    bot_id: str
    user_id: str

    # kitescratch-end

class BotCommands(BotCommandsBase):
    """Represents a command attached to a bot"""

    bot_id: str
    """The commands bot ID"""

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
        return [cls.to(e) for e in obj if e]

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
            name=tag["id"].replace("_", " ").title(),
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

    state: BotServerState
    """The bot's state"""

    flags: list[BotServerFlag]
    """The bot's flags"""

    commands: list[BotCommands]
    """The bot's commands"""

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

    flags: list[BotServerFlag]
    """The bot's/server's flags"""

    banner_card: Optional[str]
    """The bot's/server's banner_card"""

    state: BotServerState
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