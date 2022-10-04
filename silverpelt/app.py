import asyncio
from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import msgpack
import discord
from ruamel.yaml import YAML
import aioredis
from pydantic import BaseModel

from silverpelt.types.types import IDiscordUser, Status, check_snow

# We use messagepack for serialization
class MsgpackResponse(JSONResponse):
    media_type = "application/x-msgpack"

    def render(self, content: Any) -> bytes:
        return msgpack.packb(content)


app = FastAPI(default_response_class=MsgpackResponse)
bot = discord.Client(intents=discord.Intents(guilds=True, members=True, presences=True))


@bot.event
async def on_ready():
    print("Connected to discord successfully!")


yaml = YAML()

with open("config.yaml") as doc:
    config: dict = yaml.load(doc)

redis = aioredis.from_url(config["redis_url"])


async def cache(value: Any, *, key: str, expiry: int = 8 * 60 * 60) -> Any:
    """Cache a value in redis (8 hours is default for expiry)"""
    if isinstance(value, BaseModel):
        value = value.dict()
    await redis.set(key, msgpack.packb(value), ex=expiry)
    return value


@app.on_event("startup")
async def start_bot():
    asyncio.create_task(bot.start(config["secrets"]["token"]))


@app.get("/@me")
async def about_me():
    await bot.wait_until_ready()

    return IDiscordUser(
        id=bot.user.id,
        username=bot.user.name,
        disc=bot.user.discriminator,
        avatar=bot.user.avatar.url,
        bot=bot.user.bot,
        system=bot.user.system,
        status=Status.online.value,
        flags=bot.user.public_flags.value,
    )


@app.get("/users/{id}")
async def get_user(id: int):
    """Get a user from discord"""

    # An explanation on snowflakes
    """
    Joghurt

    a 16 digit number would have been created before Jan 28th, 2015, and Discord started on May 13th, 2015.
    So in practice IDs will have between 17 and 19 digits
    """
    if not check_snow(id):
        return None

    # Check if in redis cache
    user = await redis.get(f"user:{id}")

    if user:
        user_obj = msgpack.unpackb(user)

        return IDiscordUser(**user_obj) if user_obj else None
    print("Not in cache, fetching from discord")
    await bot.wait_until_ready()

    # Check if in dpy cache
    for guild in bot.guilds:
        print(guild)
        if user := guild.get_member(id):
            return await cache(
                IDiscordUser(id=user.id,username=user.name,disc=user.discriminator,
                    avatar=user.avatar.url if user.avatar else user.default_avatar.url,
                    bot=user.bot,
                    system=user.system,
                    status=Status.new(user.status.value),
                    flags=user.public_flags.value,
                ),
                key=f"user:{id}",
            )

    # Fetch from API
    try:
        print("fetching")
        user = await bot.fetch_user(id)
        return await cache(
            IDiscordUser(
                id=user.id,
                username=user.name,
                disc=user.discriminator,
                avatar=user.avatar.url if user.avatar else user.default_avatar.url,
                bot=user.bot,
                system=user.system,
                status=Status.offline,
                flags=user.public_flags.value,
            ),
            key=f"user:{id}",
        )
    except Exception as exc:
        print(exc)
        await cache(None, key=f"user:{id}", expiry=60)
        return None


@app.get("/roles/{gid}/{uid}")
async def get_guild_member_roles(gid: int, uid: int):
    guild = bot.get_guild(gid)
    if not guild:
        return None
    member = guild.get_member(uid)
    if not member:
        return None
    return [role.id for role in member.roles]
