from fates import models
from . import tables
from . import tags
import inspect
import piccolo
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette.routing import Mount
from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder

from mapleshade import Mapleshade, SilverNoData
import silverpelt.types.types as silver_types

_tables = []

tables_dict = vars(tables)

for obj in tables_dict.values():
    if obj == tables.Table:
        continue
    if inspect.isclass(obj) and isinstance(obj, piccolo.table.TableMetaclass):
        _tables.append(obj)

app = FastAPI(
    default_response_class=ORJSONResponse,
    routes=[
        Mount(
            "/admin/",
            create_admin(
                tables=_tables,
                site_name="Fates Admin",
                production=True,
                # Required when running under HTTPS, change when done
                allowed_hosts=["rewrite.fateslist.xyz"],
            ),
        ),
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "PATCH" "DELETE", "OPTIONS"],
    allow_headers=["Frostpaw-Auth"],
    allow_credentials=True,
)

mapleshade = Mapleshade()


@app.on_event("startup")
async def open_database_connection_pool():
    engine = engine_finder()
    # asyncio.create_task(bot.start(secrets["token"]))
    # await bot.load_extension("jishaku")
    await engine.start_connnection_pool()


@app.on_event("shutdown")
async def close_database_connection_pool():
    engine = engine_finder()
    await engine.close_connnection_pool()


@app.get("/bots/{bot_id}", tags=[tags.bot], response_model=models.Bot)
async def get_bot(bot_id: int):
    bot = await mapleshade.bot(bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Not Found")
    return bot


@app.get("/test/@me", response_model=silver_types.DiscordUser)
async def test_sv_resp():
    req = await mapleshade.silverpelt_req("@me")
    return req


@app.get("/blazefire/{id}", response_model=silver_types.DiscordUser)
async def get_discord_user(id: int):
    try:
        req = await mapleshade.silverpelt_req(f"users/{id}")
    except SilverNoData:
        raise HTTPException(status_code=404, detail="Not Found")
    return req
