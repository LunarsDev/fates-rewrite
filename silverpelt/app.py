import asyncio
import os
from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import msgpack
import discord
from ruamel.yaml import YAML
import aioredis
from pydantic import BaseModel

from silverpelt.types.types import ChannelMessage, IDiscordUser, Status, check_snow

from libcommon import config

# We use messagepack for serialization
class MsgpackResponse(JSONResponse):
    """We use messagepack for serialization"""

    media_type = "application/x-msgpack"

    def render(self, content: Any) -> bytes:
        """Renders the content"""
        return msgpack.packb(content)


app = FastAPI(default_response_class=MsgpackResponse)

bot = discord.Client(intents=discord.Intents(guilds=True, members=True, presences=True))


@bot.event
async def on_ready():
    """When the bot is ready, inform the user via the console"""
    print("Connected to discord successfully!")

# Construct redis URL
redis_url = f"redis://{config['storage']['redis']['host'] or os.getenv('REDIS_HOST') or 'localhost'}:{config['storage']['redis']['port'] or os.getenv('REDIS_PORT') or 6379}"

redis = aioredis.from_url(
    redis_url,
    db=config["storage"]["redis"]["database"] or 0,
    password=config["storage"]["redis"]["password"] or None,
)


async def cache(value: Any, *, key: str, expiry: int = 8 * 60 * 60) -> Any:
    """Cache a value in redis (8 hours is default for expiry)"""
    if isinstance(value, BaseModel):
        value = value.dict()
    await redis.set(key, msgpack.packb(value), ex=expiry)
    return value


@app.on_event("startup")
async def start_bot():
    """Starts the bot"""
    asyncio.create_task(bot.start(config["secrets"]["token"]))


@app.get("/@me")
async def about_me():
    """Returns information about the bot itself"""
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
                IDiscordUser(
                    id=user.id,
                    username=user.name,
                    disc=user.discriminator,
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
    """Get a user's roles from a guild"""
    guild = bot.get_guild(gid)
    if not guild:
        return None
    member = guild.get_member(uid)
    if not member:
        return None
    return [role.id for role in member.roles]


@app.post("/channel_msg")
async def send_channel_message(data: ChannelMessage):
    """Send a message to a channel"""
    channel = bot.get_channel(data.channel_id)
    if not channel:
        return None
    msg = await channel.send(
        content=data.content, embeds=[discord.Embed.from_dict(e) for e in data.embeds]
    )

    return {
        "content": msg.content,
        "embeds": [e.to_dict() for e in msg.embeds],
        "id": msg.id,
        "channel_id": msg.channel.id,
        "author": {
            "id": msg.author.id,
            "username": msg.author.name,
            "disc": msg.author.discriminator,
            "avatar": msg.author.avatar.url
            if msg.author.avatar
            else msg.author.default_avatar.url,
            "bot": msg.author.bot,
            "system": msg.author.system,
            "status": Status.new(msg.author.status.value),
            "flags": msg.author.public_flags.value,
        },
    }


@app.get("/guild_inf/{id}")
async def guild_info(id: int):
    """Check if a guild exists and return some info about it."""
    guild = bot.get_guild(id)
    return {
        "found": guild is not None,
        "invitable_channels": [
            channel.id
            for channel in guild.channels
            if channel.type
            in (
                discord.ChannelType.text,
                discord.ChannelType.news,
                discord.ChannelType.news_thread,
            )
            and channel.permissions_for(guild.me).create_instant_invite
        ]
        if guild
        else None,
    }


@app.get("/guild_invite/{id}/{channel_id}")
async def guild_invite(id: int, channel_id: int, for_user: int):
    """Create an invite to a guild."""
    guild = bot.get_guild(id)
    if not guild:
        return None
    channel = guild.get_channel(channel_id)
    if not channel:
        return None
    invite = await channel.create_invite(
        max_age=60 * 15,
        max_uses=1,
        unique=True,
        reason=f"Invite requested by {for_user or 'anonymous user'}",
    )
    return {"url": invite.url}
