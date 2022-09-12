from typing import Optional
from .tables import Bots, Users, UserBotLogs
from piccolo.utils.pydantic import create_pydantic_model

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

class Bot(BotBase):
    """Represents a bot"""
    # These fields have the wrong type set for API response, change them
    bot_id: str
    verifier: Optional[str]
    extra_links: dict

    # Raw description and long description
    long_description_raw: str

    # Other fields
    action_logs: list[UserBotLog]

class User(UserBase):
    pass