from pydantic import BaseModel, validator
import discord

class DiscordUser(BaseModel):
    id: int
    username: str
    disc: str
    avatar: str
    bot: bool
    system: bool
    status: discord.Status
    flags: int

    @validator("status")
    def status_validator(cls, v: discord.Status):
        if v == discord.Status.online:
            return "online"
        elif v == discord.Status.idle:
            return "idle"
        elif v == discord.Status.dnd:
            return "dnd"
        elif v == discord.Status.offline:
            return "offline"
        return "offline"

    class Config:
        arbitrary_types_allowed = True