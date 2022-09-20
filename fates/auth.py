from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader

from fates import tables
from fates.enums import TargetType
from .models import AuthData
from fastapi.exceptions import HTTPException

frostpaw_auth = APIKeyHeader(name="Frostpaw-Auth", description="**Format**: user/bot/server|ID|TOKEN", auto_error=False)

async def auth(header: str = Depends(frostpaw_auth)):
    try:
        auth_type, id, token = header.split("|")
    except:
        raise HTTPException(400, detail="Invalid Frostpaw-Auth header set")

    try:
        id = int(id)
    except:
        raise HTTPException(400, detail="Invalid Frostpaw-Auth header set [id is not int]")
    
    if auth_type == "user":
        auth_data = await tables.Users.select(tables.Users.api_token).where(tables.Users.user_id == id).first()

        if not auth_data:
            raise HTTPException(404, detail="User not found")
        
        if auth_data["api_token"] != token:
            raise HTTPException(401, detail="Invalid token")
        
        return AuthData(user_id=id, target_id=id, auth_type=TargetType.User)
    elif auth_type == "bot":
        auth_data = await tables.Bots.select(tables.Bots.api_token).where(tables.Bots.bot_id == id).first()

        if not auth_data:
            raise HTTPException(404, detail="Bot not found")
        
        if auth_data["api_token"] != token:
            raise HTTPException(401, detail="Invalid token")
        
        return AuthData(user_id=id, target_id=id, auth_type=TargetType.Bot)
    elif auth_type == "server":
        auth_data = await tables.Servers.select(tables.Servers.api_token).where(tables.Servers.server_id == id).first()

        if not auth_data:
            raise HTTPException(404, detail="Server not found")
        
        if auth_data["api_token"] != token:
            raise HTTPException(401, detail="Invalid token")
        
        return AuthData(user_id=id, target_id=id, auth_type=TargetType.Server)