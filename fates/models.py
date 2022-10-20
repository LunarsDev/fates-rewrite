import datetime
from typing import Any, Literal, Optional, Generic, TypeVar
import uuid

from libcommon.tables import (
    BotCommands,
    BotListTags,
    Bots,
    Users,
    UserBotLogs,
    Servers,
    Features,
    Vanity as VanityTable,
)
from piccolo.utils.pydantic import create_pydantic_model
from piccolo.query import Select
from pydantic import BaseModel, validator
from pydantic.generics import GenericModel
import silverpelt.types.types as silver_types
from libcommon.enums import *
from libcommon import config
from piccolo.columns.combination import WhereRaw

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

SERVER_SNIPPET_COLS = (
    Servers.guild_id,
    Servers.votes,
    Servers.description,
    Servers.flags,
    Servers.guild_count,
    Servers.banner_card,
    Servers.state,
)

DEFAULT_USER_EXPERIMENTS = [
    UserExperiment.UserVotePrivacy,
    UserExperiment.LynxExperimentRolloutView,
    UserExperiment.BotReport,
]


async def augment(c: Select, aug: str):
    """Augment a SQL select with custom SQL"""
    return await Bots.raw(str(c) + aug)


class UserBotLog(UserBotLogsBase):  # type: ignore[valid-type, misc]
    """A user bot log derived from the UserBotLogs table"""

    bot_id: str
    user_id: str


class BotCommands(BotCommandsBase):
    """Represents a command attached to a bot"""

    bot_id: str
    """The commands bot ID"""


class Entity:
    """Base class for all entities"""

    id: str
    """The entity's ID"""

    @staticmethod
    def to(_: dict) -> "Entity":
        """Converts a dict to an entity"""
        pass

    @classmethod
    def to_list(cls, obj: list[dict]) -> list["Entity"]:
        """Converts a list of dicts to a list of entities"""
        return [cls.to(e) for e in obj if e]

    def __eq__(self, other):
        """Checks if two entities are equal based on ID"""
        if getattr(other, "id", None):
            return self.id == getattr(other, "id", None)
        return self.id == other


class ResolvedPackBot(BaseModel):
    """Represents a bot that is part of a pack"""

    user: silver_types.DiscordUser
    """The bot's user"""

    description: str
    """The bot's description"""


class BotPack(BaseModel):
    """Represents a bot pack on the list"""

    id: uuid.UUID
    """The pack's ID"""

    name: str
    """The pack's name"""

    description: str
    """The pack's description"""

    icon: str
    """The pack's icon"""

    banner: str | None = None
    """The pack's banner"""

    resolved_bots: list[ResolvedPackBot]
    """The bots in the pack"""

    owner: silver_types.DiscordUser
    """The pack's owner"""

    created_at: datetime.datetime
    """The pack's creation date"""


class Permission(BaseModel):
    """A permission for a staff member on the list"""

    index: int
    roles: list[str]
    name: str

    def __eq__(self, other: "Permission") -> bool:
        """Check if two permissions are equal based on their index"""

        if not isinstance(other, Permission):
            return False
        return self.index == other.index

    def __lt__(self, other: "Permission") -> bool:
        """Check if a permission is less than another based on their index"""
        if not isinstance(other, Permission):
            return False
        return self.index < other.index

    def __gt__(self, other: "Permission") -> bool:
        """Check if a permission is greater than another based on their index"""
        if not isinstance(other, Permission):
            return False
        return self.index > other.index

    def __le__(self, other: "Permission") -> bool:
        """Check if a permission is less than or equal to another based on their index"""
        if not isinstance(other, Permission):
            return False
        return self.index <= other.index

    def __ge__(self, other: "Permission") -> bool:
        """Check if a permission is greater than or equal to another based on their index"""
        if not isinstance(other, Permission):
            return False
        return self.index >= other.index


class PermissionList(BaseModel):
    """A list of permissions for a staff member on the list"""

    perms: dict[str, Permission]


class Tag(BaseModel, Entity):
    """Represents a tag"""

    id: str
    """The tag's ID"""

    iconify_data: str
    """The tag's iconify class"""

    name: str
    """The tag name"""

    owner_guild: str | None = None
    """The guild ID of the tags owner (server only)"""

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


class Bot(BotBase):  # type: ignore[misc, valid-type]
    """Represents a bot"""

    user: silver_types.DiscordUser
    """The bot's user object"""

    owners: list[Owner]
    """The bot's owners"""

    # These fields have the wrong type set for API response, change them
    bot_id: str

    verifier: str | None = None
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

    banner_card: str | None = None
    """The bot's/server's banner_card"""

    state: BotServerState
    """The bot's/server's state"""

    guild_count: int
    """The bot's/server's guild count"""


class ProfileSnippet(BaseModel):
    """
    Represents a snippet which is essentially a miniature version of a profile where a full Profile is too expensive to return

    - This applies to both ``User`` entities
    """

    user: silver_types.DiscordUser
    """The user's user object"""

    banner: str | None = None
    """The user's banner"""

    description: str
    """The user's description"""


class Index(BaseModel):
    """Represents an index"""

    new: list[Snippet]
    """New bots/servers"""

    top_voted: list[Snippet]
    """Top voted bots/servers"""

    certified: list[Snippet]
    """Certified bots/servers this week"""


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


class BotSecrets(BaseModel):
    """Represents a bot's secrets"""

    api_token: str
    """The bot's API token"""

    webhook: str | None = None
    """The bot's webhook"""

    webhook_secret: str | None = None
    """The bot's webhook secret"""


class Vanity(BaseModel):
    """Represents a vanity"""

    target_id: str
    """The vanity's target ID"""

    target_type: TargetType
    """The vanity's target type"""

    code: str
    """The vanity's code"""


class Login(BaseModel):
    """Represents a login"""

    code: str
    """The Discord OAuth2 code"""


class OauthUser(BaseModel):
    """OAuth2 login response"""

    state: UserState
    """The user's state"""

    token: str
    """The user's token. If in data_action login mode, this will be the ticket for the action instead"""

    user: silver_types.DiscordUser
    """The user's user object"""

    site_lang: str
    """The user's site language"""

    css: str | None = None
    """The user's CSS"""

    user_experiments: list[UserExperiment]
    """The user's experiments"""

    permissions: Permission
    """The user's permissions"""


class OAuth2Login(BaseModel):
    """OAuth2 login response"""

    state: str
    """The user's state"""

    url: str
    """The url to redirect to"""


class Invite(BaseModel):
    """A invite for a bot/server"""

    invite: str


class ResponseCode(Enum):
    """A API response code (can be used for programatic error handling)"""

    OK = "ok"
    AUTH_FAIL = "auth_fail"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"
    INVALID_DATA = "invalid_data"
    LOGIN_REQUIRED = "login_required"
    PRIVATE_SERVER = "private_server"
    WHITELIST_ONLY = "whitelist_only"
    BLACKLISTED = "blacklisted"
    SERVER_BLACKLISTED = "server_blacklisted"
    SERVER_STAFF_REVIEW = "server_staff_review"
    SERVER_BANNED = "server_banned"
    SERVER_NO_CHANNELS = "server_no_channels"
    INTERNAL_ERROR = "internal_error"
    BOT_ALREADY_EXISTS = "bot_already_exists"
    PREFIX_TOO_LONG = "prefix_too_long"
    NO_VANITY = "no_vanity"
    VANITY_TAKEN = "vanity_taken"
    INVALID_INVITE_PERMS = "invalid_invite_perms"
    INVALID_INVITE = "invalid_invite"
    INVALID_DESCRIPTION = "invalid_description"
    INVALID_LONG_DESCRIPTION = "invalid_long_description"
    BOT_NOT_FOUND = "bot_not_found"
    NO_TAGS = "no_tags"
    TOO_MANY_TAGS = "too_many_tags"
    TOO_MANY_FEATURES = "too_many_features"
    EDIT_LOCKED = "edit_locked"
    TOO_MANY_OWNERS = "too_many_owners"
    CLIENT_ID_NEEDED = "client_id_needed"
    INVALID_CLIENT_ID = "invalid_client_id"
    PRIVATE_BOT = "private_bot"
    INVALID_OWNERS = "invalid_owners"
    EXTRA_LINK_VAL_LENGTH_ERR = "extra_link_val_length_err"
    EXTRA_LINK_KEY_LENGTH_ERR = "extra_link_key_length_err"
    EXTRA_LINK_NOT_HTTP = "extra_link_not_http"
    TOO_MANY_RENDERABLE_EXTRA_LINKS = "too_many_renderable_extra_links"
    TOO_MANY_EXTRA_LINKS = "too_many_extra_links"
    INVALID_BANNER_PAGE = "invalid_banner_page"
    INVALID_BANNER_CARD = "invalid_banner_card"
    ANTI_ABUSE_ERROR = "anti_abuse_error"
    NOT_MAIN_OWNER = "not_main_owner"
    INVALID_FLAG = "invalid_flag"
    VOTED_RECENTLY = "voted_recently"
    SYSTEM_BOT_VOTE = "system_bot_vote"
    VOTE_AUTOROLE_ERROR = "vote_autorole_error"
    NOT_IMPLEMENTED = "not_implemented"
    COMMAND_LENGTH_ERR = "command_length_err"
    STAR_RATING_ERR = "star_rating_err"
    INVALID_REVIEW_TEXT = "invalid_review_text"
    TOO_MANY_REVIEWS = "too_many_reviews"
    INVALID_PARENT_REVIEW = "invalid_parent_review"
    REVIEW_ALR_VOTED = "review_alr_voted"
    INVALID_APPEAL_TEXT = "invalid_appeal_text"
    BOT_NOT_APPROVED = "bot_not_approved"
    CERT_NO_BANNER_CARD = "cert_no_banner_card"
    CERT_NO_BANNER_PAGE = "cert_no_banner_page"
    TOO_FEW_GUILDS = "too_few_guilds"
    TOO_FEW_MEMBERS = "too_few_members"
    BAD_STATS = "bad_stats"
    TOO_MANY_SUBSCRIPTIONS = "too_many_subscriptions"
    TOO_MANY_BOTS_FOR_PACK = "too_many_bots_for_pack"
    INVALID_BOT_ID_FOR_PACK = "invalid_bot_id_for_pack"
    TOO_FEW_BOTS_FOR_PACK = "too_few_bots_for_pack"
    INVALID_ICON_FOR_PACK = "invalid_icon_for_pack"
    INVALID_BANNER_FOR_PACK = "invalid_banner_for_pack"


class Response(BaseModel):
    """A API Response"""

    done: bool
    """Whether or not the request was successful"""

    code: Optional[ResponseCode] = ResponseCode.OK
    """The response code (can be used for programatic error handling)"""

    reason: str | None = None
    """The reason for the request failing (if any)"""

    data: Optional[dict] = None
    """Extra data (if any)"""

    @staticmethod
    def ok():
        """Returns a successful response"""
        return Response(done=True, code=ResponseCode.OK)

    def error(self, status_code: int):
        """Raises a error response which is then caught by the exception handler"""
        raise ResponseRaise(self, status_code)

    @staticmethod
    def not_implemented():
        """Raises a not implemented response"""
        Response(
            done=False,
            code=ResponseCode.UNKNOWN,
            reason="This feature/endpoint is not implemented yet",
        ).error(
            409
        )  # Conflict

    @staticmethod
    def invalid_auth_type(target_type: TargetType):
        """Raises an invalid auth type response"""
        if target_type == TargetType.Bot:
            Response(
                done=False,
                code=ResponseCode.AUTH_FAIL,
                reason="Bot-only endpoint",
            ).error(401)
        elif target_type == TargetType.User:
            Response(
                done=False,
                code=ResponseCode.AUTH_FAIL,
                reason="User-only endpoint",
            ).error(401)
        elif target_type == TargetType.Server:
            Response(
                done=False,
                code=ResponseCode.AUTH_FAIL,
                reason="Server-only endpoint",
            ).error(401)
        else:
            Response(
                done=False,
                code=ResponseCode.AUTH_FAIL,
                reason="Target type cannot be authenticated",
            ).error(401)


class ResponseRaise(Exception):
    """Raised via ``Response.error``"""

    def __init__(self, response: Response, status_code: int):
        self.status_code = status_code
        self.response = response


# Test model
class NestedModel(BaseModel):
    """A nested model"""

    test: str
    """A test field"""

    perms: Permission
    """A permission field"""


class TaskResponse(BaseModel):
    """A created task response"""

    task_id: str
    """The task ID"""


class AuthData(BaseModel):
    """INTERNAL: Auth struct"""

    auth_type: TargetType
    target_id: int
    token: str
    compat: bool


class AuthDataHTTPResponse(AuthData):
    """AuthData struct for HTTP responses"""

    target_id: str


DataT = TypeVar("DataT")


class SearchFilter(GenericModel, Generic[DataT]):
    """A filter for search"""

    filter_from: DataT
    """The value to filter from"""

    filter_to: DataT
    """The value to filter to"""

    def __iter__(self):
        """Yields the filter which can then be unpacked using * notation"""
        yield self.filter_from
        yield self.filter_to


class SearchTags(BaseModel):
    """Filter by tag"""

    bot: list[str] = []
    """Bot tags"""

    server: list[str] = []
    """Server tags"""

    bot_op: Literal["@>", "&&"] = "@>"
    """Bot tag operator: @> = all, && = any"""

    server_op: Literal["@>", "&&"] = "@>"
    """Server tag operator: @> = all, && = any"""


class SearchQuery(BaseModel):
    """A search query"""

    query: str
    """The search query"""

    guild_count: SearchFilter[int] = SearchFilter[int](filter_from=0, filter_to=-1)
    """The guild count filter"""

    votes: SearchFilter[int] = SearchFilter[int](filter_from=0, filter_to=-1)
    """The vote count filter"""

    tags: SearchTags = SearchTags()
    """The tags filter"""


class SearchResponse(BaseModel):
    """A search response"""

    bots: list[Snippet]
    """The bots that matched the search query"""

    servers: list[Snippet]
    """The servers that matched the search query"""

    profiles: list[ProfileSnippet]
    """The profiles that matched the search query"""

    packs: list[BotPack]


class BotAddTicket(BaseModel):
    """Bot add ticket response"""

    ticket: str
    """The ticket ID"""

    bot_id: str
    """The bot ID we found"""

    data: dict[str, Any]
    """The bot data we found"""


class BotUpdate(BaseModel):
    """Bot update data (common set of validation for add/edit bot) [For edit bot, inherit from both BotUpdate and Bot]"""

    tags: list[str]
    """The tags to of the bot"""

    features: list[str]
    """The features to of the bot"""

    prefix: str | None = None
    """The prefix of the bot"""

    description: str
    """The description of the bot"""

    long_description_type: LongDescriptionType
    """The long description type"""

    long_description: str
    """The long description of the bot"""

    invite: str | None = None
    """The invite of the bot. Set to none for autogenerated invite"""

    vanity: str

    @validator("prefix")
    def validate_prefix(cls, v):
        """Ensure prefix is either a value or None"""
        if not v:
            return None
        elif len(v) > 10:
            raise ValueError("Prefix cannot be longer than 10 characters")
        return v

    @validator("invite")
    def validate_invite(cls, v: str):
        """Validates the invite is https://"""
        if not v:
            return None

        if not v.startswith("https://"):
            raise ValueError("Invites must start with https://")
        return v

    @validator("description")
    def validate_description(cls, v: str):
        """Validates the description is of sufficient length"""
        if len(v) > 100:
            raise ValueError("Description must be less than 100 characters")
        elif len(v) < 10:
            raise ValueError("Description must be more than 10 characters")
        return v

    @validator("long_description")
    def validate_long_description(cls, v: str):
        """Validates the long description is of sufficient length"""
        if len(v) < 100:
            raise ValueError("Long description must be more than 100 characters")
        return v

    @validator("tags")
    def validate_tags(cls, v: list[str]):
        """Validates the tags are of sufficient length"""
        if len(v) > 10:
            raise ValueError("You can only have a maximum of 10 tags")
        elif len(v) < 1:
            raise ValueError("You must have at least 1 tag")
        return v

    @validator("features")
    def validate_features(cls, v: list[str]):
        """Validates no more than 10 features are provided"""
        if len(v) > 10:
            raise ValueError("You can only have a maximum of 10 features")
        return v

    @validator("vanity")
    def validate_vanity(cls, v: str):
        """Validates the vanity is valid"""
        if len(v) > 64:
            raise ValueError("Vanity must be less than 64 characters")
        elif v in RESTRICTED_VANITY:
            raise ValueError("Vanity is restricted and cannot be used")
        elif not v:
            raise ValueError("Vanity cannot be empty")
        return v

    async def db_validate(self):
        """Validates that all tags and features are valid and in the database"""
        for tag in self.tags:
            if not await BotListTags.exists().where(BotListTags.id == tag):
                Response(
                    done=False,
                    code=ResponseCode.INVALID_DATA,
                    reason=f"Tag {tag} does not exist",
                ).error(400)

        for feature in self.features:
            if not await Features.exists().where(Features.id == feature):
                Response(
                    done=False,
                    code=ResponseCode.INVALID_DATA,
                    reason=f"Feature {feature} does not exist",
                ).error(400)

        vanity = (
            await VanityTable.select()
            .where(WhereRaw("lower(vanity_url) = {}", self.vanity.lower()))
            .first()
        )

        if vanity:
            Response(
                done=False,
                code=ResponseCode.INVALID_DATA,
                reason=f"Vanity {self.vanity} already exists",
            ).error(400)


class BotAddFinalize(BotUpdate):
    """Bot add finalize response"""

    ticket: str
    """The ticket from the add ticket response"""


class PreviewData(BaseModel):
    """Preview data for websocket"""

    type: LongDescriptionType
    """The type of long description"""

    content: str
    """The content of the long description"""


# Constants for the bot list
DEFAULT_EXC = {404: ResponseCode.NOT_FOUND}
RESTRICTED_VANITY: list[str] = config["misc"]["restricted_vanity"]
