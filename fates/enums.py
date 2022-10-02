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

    EditLocked = 1, "Bot or server is locked and cannot be editted but can be unlocked by the owner"

    StaffLocked = 2, "Bot or server is locked by staff and can only be unlocked by staff"

    StatsLocked = 3, "Bot or server stats are locked due to abuse"

    VoteLocked = 4, "Bot or server is locked from voting due to abuse"

    System = 5, "Bot or server is a system bot or server"

    WhitelistOnly = 6, "Server is a whitelist only server (it cannot be joined without being whitelisted by staff on said server)"

    KeepBannerDecor = 7, "Bot or server banner should keep special fallback banner styles"

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

    Normal = 0, "User is normal (no bans)"

    GlobalBan = 1, "User is globally banned from the list (apart from data actions)"

    ProfileEditBan = 2, "User is banned from editing their profile due to abuse"


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
    User = 2


class PageStyle(IntEnum):
    tabs = 0
    single_scroll = 1

class UserExperiment(IntEnum):
    """User experiments"""
    _init_ = "value __doc__"

    Unknown = 0, "Unknown experiment"

    GetRoleSelector = 1, "We switched to native roles. This experiment FAILED"

    LynxExperimentRolloutView = 2, "Lynx experiment rollout view. No longer relevant"

    BotReport = 3, "Bot reports are supported"
    
    ServerAppealCertification = 4, "Ability to use request type of Appeal or Certification in server appeal"

    UserVotePrivacy = 5, "The ability for users to hide their votes from Get Bot Votes and Get Server Votes API"

    DevPortal = 6, "The ability to use the developer portal. No longer relevant"


class DataAction(Enum):
    """Data actions"""

    Request = "req"
    """Unknown action"""

    Delete = "del"
    """Create action"""