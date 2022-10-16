import enum
from pydantic import BaseModel, root_validator


class Status(enum.IntEnum):
    """Represents a users status"""

    online = 0
    idle = 1
    dnd = 2
    offline = 3

    @classmethod
    def new(cls, v):
        """Returns a new status enum based on the value"""
        # https://www.reddit.com/r/Python/comments/ur9t92/python_310_match_statements_are_86_faster_than_if/
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


def check_snow(id: int) -> bool:
    """Checks if a snowflake is valid"""
    return len(str(id)) >= 17 and len(str(id)) <= 20


class ChannelMessage(BaseModel):
    """Represents a channel message that is sent to the client"""

    channel_id: int

    embeds: list[dict] = []

    content: str = ""

    @root_validator(pre=True)
    def ensure_one_of_embeds_content(cls, values: dict):
        """Ensures that either embeds or content is set"""
        if not values.get("embeds") and not values.get("content"):
            raise ValueError("Either embeds or content must be set")

        elif len(values.get("embeds", [])) > 10:
            raise ValueError("Cannot have more than 10 embeds")

        elif len(values.get("content", "")) > 2000:
            raise ValueError("Content cannot be more than 2000 characters")

        return values
