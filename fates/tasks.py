from fates import tables

async def data_delete(user_id: int):
    """Delete a user's data"""
    # TODO: Handle bot/server votes checks of lynx
    # TODO: Also handle global ban and other ban cases
    await tables.Users.delete().where(tables.Users.user_id == user_id)

    # Delete all bot data of a user
    bots = await tables.Users.raw(
        """SELECT DISTINCT bots.bot_id FROM bots 
        INNER JOIN bot_owner ON bot_owner.bot_id = bots.bot_id 
        WHERE bot_owner.owner = {} AND bot_owner.main = true""",
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

    return {    
        "detail": "All found user data deleted"
    }
