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

UserBotLogs = create_pydantic_model(UserBotLogs, deserialize_json=True)

class Bot(BotBase):
    """Represents a bot"""
    # These fields have to be str and not int
    bot_id: str
    verifier: str

    # Raw description and long description
    long_description_raw: str

    # Other fields
    action_logs: list[UserBotLogs]

class User(UserBase):
    pass