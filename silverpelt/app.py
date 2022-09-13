import asyncio
from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import msgpack
import discord
from ruamel.yaml import YAML

from silverpelt.types.types import DiscordUser

# We use messagepack for serialization
class MsgpackResponse(JSONResponse):
    media_type = "application/x-msgpack"

    def render(self, content: Any) -> bytes:
        return msgpack.packb(content)

app = FastAPI(default_response_class=MsgpackResponse)
bot = discord.Client(intents=discord.Intents(guilds=True, members=True, presences=True))

yaml = YAML()

with open("config.yaml") as doc:
    config: dict = yaml.load(doc)

@app.on_event("startup")
async def start_bot():
    asyncio.create_task(bot.start(config["secrets"]["token"]))

@app.get("/@me")
async def about_me():
    return DiscordUser(
        id=bot.user.id,
        username=bot.user.name,
        disc=bot.user.discriminator,
        avatar=bot.user.avatar.url,
        bot=bot.user.bot,
        system=bot.user.system,
        status=discord.Status.online.value,
        flags=bot.user.public_flags.value
    )