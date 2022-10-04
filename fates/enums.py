from aenum import IntEnum, StrEnum as Enum


class WidgetFormat(Enum):
    """Widget format"""

    _init_ = "value __doc__"

    json = "json", "Raw JSON format"

    html = "html", "HTML format"

    png = "png", "PNG image format. May produce better results than WEBP"

    webp = "webp", "WebP image format"


class BotServerFlag(IntEnum):
    """Flags that apply to both bots and servers"""

    _init_ = "value __doc__"

    Unlocked = 0, "Bot or server is unlocked and can be freely editted"

    EditLocked = (
        1,
        "Bot or server is locked and cannot be editted but can be unlocked by the owner",
    )

    StaffLocked = (
        2,
        "Bot or server is locked by staff and can only be unlocked by staff",
    )

    StatsLocked = 3, "Bot or server stats are locked due to abuse"

    VoteLocked = 4, "Bot or server is locked from voting due to abuse"

    System = 5, "Bot or server is a system bot or server"

    WhitelistOnly = (
        6,
        "Server is a whitelist only server (it cannot be joined without being whitelisted by staff on said server)",
    )

    KeepBannerDecor = (
        7,
        "Bot or server banner should keep special fallback banner styles",
    )

    NSFW = 8, "Bot or server is NSFW"

    LoginRequired = 9, "Server requires the user to be logged in to join"


class UserFlag(IntEnum):
    """Flags that apply to users"""

    _init_ = "value __doc__"

    Unknown = 0, "Unknown flag"

    VotesPrivate = 1, "User's votes are private"

    Staff = 2, "User is a staff member"

    AvidVoter = 3, "User is an avid voter"


class UserState(IntEnum):
    """User states"""

    _init_ = "value __doc__"

    Normal = 0, "User is normal (not banned)"

    GlobalBan = 1, "User is globally banned from the list (apart from data actions)"

    ProfileEditBan = 2, "User is banned from editing their profile due to abuse"


class BotServerState(IntEnum):
    """Bot or server state"""

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


class UserBotAction(IntEnum):
    """Actions a user can take on a bot"""

    Approve = 0
    Deny = 1
    Certify = 2
    Ban = 3
    Claim = 4
    Unclaim = 5
    TransferOwnership = 6
    EditBot = 7
    DeleteBot = 8
    Unban = 9
    Uncertify = 10
    Unverify = 11
    Requeue = 12


class LongDescriptionType(IntEnum):
    """The type of long description. This is used to determine how the long description should be processed/rendered"""

    _init_ = "value __doc__"

    Html = 0, "Raw HTML. No markdown processing is applied"

    MarkdownServerSide = (
        1,
        "Markdown. Markdown is processed server side using the ``cmarkgfm`` library.",
    )


class WebhookType(IntEnum):
    """The type of webhook (Fates Client is deprecated and has no effect anymore)"""

    Vote = 0
    DiscordIntegration = 1
    DeprecatedFatesClient = 2  # There in case any bots are still using it


class CommandType(IntEnum):
    """The type of bot command"""

    PrefixCommand = 0
    SlashCommandGlobal = 1
    SlashCommandGuild = 2


class TargetType(IntEnum):
    """A bot/server/user etc."""

    Bot = 0
    Server = 1
    User = 2
    Pack = 3


class PageStyle(IntEnum):
    """Page style for the bot/server page"""

    _init_ = "value __doc__"

    Tabs = 0, "Legacy tabs style"

    SingleScroll = 1, "Single scroll/no tabs style"


class UserExperiment(IntEnum):
    """User experiments"""

    _init_ = "value __doc__"

    Unknown = 0, "Unknown experiment"

    GetRoleSelector = 1, "We switched to native roles. This experiment FAILED"

    LynxExperimentRolloutView = 2, "Lynx experiment rollout view. No longer relevant"

    BotReport = 3, "Bot reports are supported"

    ServerAppealCertification = (
        4,
        "Ability to use request type of Appeal or Certification in server appeal",
    )

    UserVotePrivacy = (
        5,
        "The ability for users to hide their votes from Get Bot Votes and Get Server Votes API",
    )

    DevPortal = 6, "The ability to use the developer portal. No longer relevant"


class DataAction(Enum):
    """Data actions"""

    Request = "req"

    Delete = "del"
