from enum import IntEnum, Enum


class WidgetFormat(Enum):
    """Widget format"""

    JSON = "json"

    HTML = "html"

    PNG = "png"

    WEBP = "webp"

    @staticmethod
    def docs():
        """Returns the docs for the enum"""
        return {
            "JSON": {
                "description": "Raw JSON format",
            },
            "HTML": {
                "description": "HTML format",
            },
            "PNG": {
                "description": "PNG image format. May produce better results than WEBP",
            },
            "WEBP": {
                "description": "WebP image format",
            },
        }


class BotServerFlag(IntEnum):
    """Flags that apply to both bots and servers"""

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

    @staticmethod
    def docs():
        """Returns the docs for the enum"""
        return {
            "Unlocked": {
                "description": "Bot or server is unlocked and can be freely editted",
            },
            "EditLocked": {
                "description": "Bot or server is locked and cannot be editted but can be unlocked by the owner",
            },
            "StaffLocked": {
                "description": "Bot or server is locked and cannot be editted but can be unlocked by staff (only)",
            },
            "StatsLocked": {
                "description": "Bot or server stats are locked due to abuse",
            },
            "VoteLocked": {
                "description": "Bot or server is locked from voting due to abuse",
            },
            "System": {
                "description": "Bot or server is a system bot or server",
            },
            "WhitelistOnly": {
                "description": "Server is a whitelist only server (it cannot be joined without being whitelisted by staff on said server)",
            },
            "KeepBannerDecor": {
                "description": "Bot or server banner should keep special fallback banner styles",
            },
            "NSFW": {
                "description": "Bot or server is NSFW",
            },
            "LoginRequired": {
                "description": "Server requires the user to be logged in to join",
            },
        }


class UserFlag(IntEnum):
    """Flags that apply to users"""

    Unknown = 0

    VotesPrivate = 1

    Staff = 2

    AvidVoter = 3

    @staticmethod
    def docs():
        """Returns the docs for the enum"""
        return {
            "Unknown": {
                "description": "Unknown flag",
            },
            "VotesPrivate": {
                "description": "User's votes are private",
            },
            "Staff": {
                "description": "User is a staff member",
            },
            "AvidVoter": {
                "description": "User is an avid voter",
            },
        }


class UserState(IntEnum):
    """User states"""

    Normal = 0

    GlobalBan = 1

    ProfileEditBan = 2

    @staticmethod
    def docs():
        """Returns the docs for the enum"""
        return {
            "Normal": {
                "description": "User is normal (not banned)",
            },
            "GlobalBan": {
                "description": "User is globally banned from the list (apart from data actions)",
            },
            "ProfileEditBan": {
                "description": "User is banned from editing their profile due to abuse",
            },
        }


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

    Html = 0

    MarkdownServerSide = 1

    @staticmethod
    def docs():
        """Returns the docs for the enum"""
        return {
            "Html": {
                "description": "Raw HTML. No markdown processing is applied",
            },
            "MarkdownServerSide": {
                "description": "Markdown supported. Markdown is processed server side using the ``cmarkgfm`` library.",
            },
        }


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

    Tabs = 0

    SingleScroll = 1

    @staticmethod
    def docs():
        """Returns the docs for the enum"""
        return {
            "Tabs": {
                "description": "Legacy tabs style",
            },
            "SingleScroll": {
                "description": "Single scroll/no tabs style",
            },
        }


class UserExperiment(IntEnum):
    """User experiments"""

    Unknown = 0

    GetRoleSelector = 1

    LynxExperimentRolloutView = 2

    BotReport = 3

    ServerAppealCertification = 4

    UserVotePrivacy = 5

    DevPortal = 6

    @staticmethod
    def docs():
        """Returns the docs for the enum"""
        return {
            "Unknown": {
                "description": "Unknown experiment",
            },
            "GetRoleSelector": {
                "description": "We switched to native roles. This experiment FAILED",
            },
            "LynxExperimentRolloutView": {
                "description": "Lynx experiment rollout view. No longer relevant",
            },
            "BotReport": {
                "description": "Bot reports are supported",
            },
            "ServerAppealCertification": {
                "description": "Ability to use request type of Appeal or Certification in server appeal",
            },
            "UserVotePrivacy": {
                "description": "The ability for users to hide their votes from Get Bot Votes and Get Server Votes API",
            },
            "DevPortal": {
                "description": "The ability to use the developer portal. No longer relevant",
            },
        }


class DataAction(Enum):
    """Data actions"""

    Request = "req"

    Delete = "del"
