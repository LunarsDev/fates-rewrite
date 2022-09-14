from enum import Enum, IntEnum


class WidgetType(Enum):
    bot = "bot"
    server = "server"


class WidgetFormat(Enum):
    json = "json"
    html = "html"
    png = "png"
    webp = "webp"


class BotServerFlag(IntEnum):
    Unlocked = 0
    EditLocked = 1
    StaffLocked = 2
    StatsLocked = 3
    VoteLocked = 4
    System = 5
    WhitelistOnly = 6
    KeepBannerDecor = 7
    NSFW = 8
    LoginRequired = 9


class UserFlag(IntEnum):
    Unknown = 0
    VotesPrivate = 1
    Staff = 2
    AvidVoter = 3


class UserState(IntEnum):
    Normal = 0
    GlobalBan = 1
    ProfileEditBan = 2

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
