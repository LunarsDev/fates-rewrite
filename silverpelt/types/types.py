from pydantic import BaseModel, validator

class DiscordUser(BaseModel):
    id: int
    username: str
    disc: str
    avatar: str
    bot: bool
    system: bool
    status: str
    flags: int