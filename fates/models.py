from .tables import Bots, Users
from piccolo.utils.pydantic import create_pydantic_model

# Add models here
Bot = create_pydantic_model(Bots, exclude_columns=[
    Bots.api_token,
    Bots.webhook_secret,
    Bots.webhook,
])
User = create_pydantic_model(Users, exclude_columns=[
    Users.api_token,
])