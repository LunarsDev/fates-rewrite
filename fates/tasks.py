from typing import Awaitable
from fates import tables
from fates.app import mapleshade
from fastapi.encoders import jsonable_encoder
import traceback


async def task(task: Awaitable, task_id: str):
    """Creates a task"""
    print(f"Starting task {task_id}")

    mapleshade.cache.set(f"task-{task_id}", "running")

    try:
        ret = await task
    except Exception as exc:
        mapleshade.cache.set(f"task-{task_id}", traceback.format_exc(exc))
        raise exc

    if not ret:
        ret = "OK"
    
    mapleshade.cache.set(f"task-{task_id}", ret)

async def data_request(user_id: int):
    user = await tables.Users.select().where(tables.Users.user_id == user_id).first()
    owners = await tables.BotOwner.select().where(tables.BotOwner.owner == user_id)

    fk_keys = await mapleshade.pool.fetch(mapleshade.sql.data_request_get_tables)

    related_data = {}

    for fk in fk_keys:
        if fk["foreign_table_name"] == "users":
            related_data[fk["table_name"]] = await tables.Users.raw(
                f"SELECT * FROM {fk['table_name']} WHERE {fk['column_name']} = {{}}", 
                user_id
            )

    data = {
        "user": user,
        "owners": owners,
        "owned_bots": [],
        "fk_keys": fk_keys,
        "related_data": related_data
    }

    for bot in owners:
        data["owned_bots"].append(
            await tables.Bots.select().where(tables.Bots.bot_id == bot["bot_id"]).first()
        )
    
    return mapleshade.parse_dict(jsonable_encoder(data))

async def data_delete(user_id: int):
    """Delete a user's data"""
    # TODO: Handle bot/server votes checks of lynx
    # TODO: Also handle global ban and other ban cases
    await tables.Users.delete().where(tables.Users.user_id == user_id)

    # Delete all bot data of a user
    bots = await mapleshade.pool.fetch(
        mapleshade.sql.data_delete_find_bots,
        user_id,
    )
    for bot in bots:
        await tables.Bots.delete().where(tables.Bots.bot_id == bot["bot_id"])
        await tables.Vanity.delete().where(tables.Vanity.redirect == bot["bot_id"])

    # Delete all vote data of a user
    votes = await tables.BotVoters.select(tables.BotVoters.bot_id).where(tables.BotVoters.user_id == user_id)
    for vote in votes:
        await tables.Bots.update(votes=tables.Bots.votes - 1).where(tables.Bots.bot_id == vote["bot_id"])

    await tables.BotVoters.delete().where(tables.BotVoters.user_id == user_id)

    votes = await tables.ServerVoters.select(tables.ServerVoters.guild_id).where(tables.ServerVoters.user_id == user_id)
    for vote in votes:
        await tables.Servers.update(votes=tables.Servers.votes - 1).where(tables.Servers.guild_id == vote["guild_id"])

    await tables.ServerVoters.delete().where(tables.ServerVoters.user_id == user_id)
