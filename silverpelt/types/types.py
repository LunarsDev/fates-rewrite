import enum
from pydantic import BaseModel

class Status(enum.IntEnum):
    online = 0
    idle = 1
    dnd = 2
    offline = 3

    @classmethod
    def new(cls, v):
        match v:
            case "online":
                return Status.online
            case "idle":
                return Status.idle
            case "dnd":
                return Status.dnd
            case "offline" | _:
                return Status.offline

class IDiscordUser(BaseModel):
    """Represents a internal silverpelt discord user response. Not safe to be returned in JS"""
    id: int
    username: str
    disc: str
    avatar: str
    bot: bool
    system: bool
    status: Status
    flags: int

class DiscordUser(IDiscordUser):
    """Represents a discord user"""
    id: str