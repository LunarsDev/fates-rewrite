from typing import Literal, Optional
from typing_extensions import Self
from .tables import Bots, Users, UserBotLogs
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel
import silverpelt.types.types as silver_types

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


class UserBotLog(UserBotLogsBase):  # type: ignore[valid-type, misc]
    bot_id: str
    user_id: str


class Entity:
    id: str
    """The entity's ID"""

    @staticmethod
    def to(_: dict) -> "Entity":
        pass

    @classmethod
    def to_list(cls, obj: list[dict]) -> list["Entity"]:
        return [cls.to(e) for e in obj]

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

    @staticmethod
    def to(tag: dict) -> "Tag":
        """Returns all tags for a bot"""
        return Tag(
            id=tag["id"],
            iconify_data=tag["icon"],
            name=tag["id"].replace("_", "").title(),
            owner_guild=tag.get("owner_guild", None),
        )


class Feature(BaseModel, Entity):
    """Represents a feature"""

    id: str
    """The feature's ID"""

    name: str
    """Feature Name"""

    viewed_as: Literal["positive", "negative"]
    """Whether the feature is viewed as positive or negative"""

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


class User(UserBase):  # type: ignore[valid-type, misc]
    pass
