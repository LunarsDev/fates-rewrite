from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader

from fates import tables
from fates import enums
from fates.enums import TargetType
from .models import AuthData, Response, ResponseCode
from fastapi.exceptions import HTTPException
import secrets

frostpaw_auth = APIKeyHeader(name="Frostpaw-Auth", scheme_name="Frostpaw-Auth", description="**Format**: user/bot/server|ID|TOKEN", auto_error=False)
compat_header = APIKeyHeader(name="Authorization", scheme_name="Bot (compat)", description="**Format**: TOKEN (*for backwards compatibility only, only some bot endpoints supported*)", auto_error=False)

async def auth(header: str = Depends(frostpaw_auth), compat: str = Depends(compat_header)):
    if compat:
        auth_data = await tables.Bots.select(tables.Bots.bot_id).where(tables.Bots.api_token == compat.replace("Bot ", "")).first()

        if not auth_data:
            Response(
                done=False,
                reason="The specified bot could not be found",
                code=ResponseCode.NOT_FOUND
            ).error(404)
                
        return AuthData(target_id=auth_data["bot_id"], auth_type=TargetType.Bot, token=compat, compat=True)

    try:
        auth_type, id, token = header.split("|")
    except:
        Response(
            done=False,
            reason="Invalid Frostpaw-Auth header set",
            code=ResponseCode.AUTH_FAIL
        ).error(400)

    try:
        id = int(id)
    except:
        Response(
            done=False,
            reason="Invalid Frostpaw-Auth header set [id is not int]",
            code=ResponseCode.AUTH_FAIL
        ).error(400)
    
    if auth_type == "user":
        auth_data = await tables.Users.select(tables.Users.api_token).where(tables.Users.user_id == id, tables.Users.state != enums.UserState.GlobalBan.value).first()

        if not auth_data:
            Response(
                done=False,
                reason="The specified user could not be found",
                code=ResponseCode.NOT_FOUND
            ).error(404)
        
        if not secrets.compare_digest(auth_data["api_token"], token):
            Response(
                done=False,
                reason="Invalid Frostpaw-Auth header set [token mismatch]",
                code=ResponseCode.AUTH_FAIL
            ).error(401)
        
        return AuthData(target_id=id, auth_type=TargetType.User, token=token, compat=False)
    elif auth_type == "bot":
        auth_data = await tables.Bots.select(tables.Bots.api_token).where(tables.Bots.bot_id == id).first()

        if not auth_data:
            Response(
                done=False,
                reason="The specified bot could not be found",
                code=ResponseCode.NOT_FOUND
            ).error(404)
        
        if not secrets.compare_digest(auth_data["api_token"], token):
            Response(
                done=False,
                reason="Invalid Frostpaw-Auth header set [token mismatch]",
                code=ResponseCode.AUTH_FAIL
            ).error(401)
        
        return AuthData(target_id=id, auth_type=TargetType.Bot, token=token, compat=False)
    elif auth_type == "server":
        auth_data = await tables.Servers.select(tables.Servers.api_token).where(tables.Servers.server_id == id).first()

        if not auth_data:
            Response(
                done=False,
                reason="The specified server could not be found",
                code=ResponseCode.NOT_FOUND
            ).error(404)
        
        if not secrets.compare_digest(auth_data["api_token"], token):
            Response(
                done=False,
                reason="Invalid Frostpaw-Auth header set [token mismatch]",
                code=ResponseCode.AUTH_FAIL
            ).error(401)
        
        return AuthData(target_id=id, auth_type=TargetType.Server, token=token, compat=False)