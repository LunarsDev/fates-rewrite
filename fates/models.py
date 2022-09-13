from typing import Optional
from .tables import Bots, Users, UserBotLogs, BotListTags
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel

# Add models here
BotBase = create_pydantic_model(Bots, deserialize_json=True, exclude_columns=(
    Bots.api_token,
    Bots.webhook_secret,
    Bots.webhook,
))
UserBase = create_pydantic_model(Users, deserialize_json=True, exclude_columns=(
    Users.api_token,
))

UserBotLogsBase = create_pydantic_model(UserBotLogs, deserialize_json=True)

class UserBotLog(UserBotLogsBase):
    bot_id: str
    user_id: str

class Tag(BaseModel):
    """Represents a tag"""
    id: str
    """The tag ID"""

    iconify_data: str
    """The tag's iconify class"""
    
    name: str
    """The tag name"""

    owner_guild: Optional[str]
    """The guild ID of the tags owner (server only)"""

    @staticmethod
    def to_tag(tag: dict) -> "Tag":
        """Returns all tags for a bot"""
        return Tag(
            id=tag["id"],
            iconify_data=tag["icon"],
            name=tag["id"].replace("_", "").title(),
            owner_guild=tag.get("owner_guild", None)
        )

    @staticmethod
    def to_tag_list(tags: list[dict]) -> "list[Tag]":
        """Returns all tags for a bot"""
        return [Tag.to_tag(tag) for tag in tags]

class Bot(BotBase):
    """Represents a bot"""
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

    tags: list[Tag]


class User(UserBase):
    pass
