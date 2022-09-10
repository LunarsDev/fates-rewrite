from enum import Enum, IntEnum

class WidgetType(Enum):
    bot = "bot"
    server = "server"

class WidgetFormat(Enum):
    json = "json"
    html = "html"
    png = "png"
    webp = "webp"
        
class BotFlag(IntEnum):
    unlocked = 0
    edit_locked = 1
    staff_locked = 2
    stats_locked = 3
    vote_locked = 4
    system = 5
    whitelist_only = 6
    keep_banner_decor = 7
    nsfw = 8

class UserFlag(IntEnum):
    Unknown = 0
    VotesPrivate = 1
    Staff = 2
    AvidVoter = 3

class UserState(IntEnum):
    normal = 0
    global_ban = 1
    profile_edit_ban = 2
    ddr_ban = 3
    api_ban = 4

# LYNX
class BotState(IntEnum):
    approved = 0
    pending = 1
    denied = 2
    hidden = 3
    banned = 4
    under_review = 5
    certified = 6
    archived = 7
    private_viewable = 8
    private_staff_only = 9

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

class LongDescType(IntEnum):
    html = 0
    markdown_serverside = 1

class WebhookType(IntEnum):
    vote = 0
    discord = 1
    fc = 2

class CommandType(IntEnum):
    regular = 0
    guild_slash = 1
    global_slash = 2

class ReviewType(IntEnum):
    bot = 0
    server = 1

class PageStyle(IntEnum):
    tabs = 0
    single_scroll = 1
