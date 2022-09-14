from fates import enums, models
from . import tables
from . import tags
import inspect
import piccolo
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, HTMLResponse
from starlette.routing import Mount
from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder

from mapleshade import Mapleshade, SilverNoData, CacheValue
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

@app.get("/index", response_model=models.Index)
async def index(target_type: enums.TargetType):
    if target_type == enums.TargetType.Bot:

        cached_index = mapleshade.cache.get("bot_index")

        if cached_index:
            return cached_index.value()
        index = models.Index(
            top_voted=await mapleshade.to_snippet(
                await tables.Bots.select(*models.BOT_SNIPPET_COLS).where(tables.Bots.state == enums.BotServerState.Approved).order_by(tables.Bots.votes, ascending=False).limit(12)
            ),
            new=await mapleshade.to_snippet(
                await tables.Bots.select(*models.BOT_SNIPPET_COLS).where(tables.Bots.state == enums.BotServerState.Approved).order_by(tables.Bots.created_at, ascending=False).limit(12)
            ),
            certified=await mapleshade.to_snippet(
                await tables.Bots.select(*models.BOT_SNIPPET_COLS).where(tables.Bots.state == enums.BotServerState.Certified).order_by(tables.Bots.votes, ascending=False).limit(12)
            ),
        )
        mapleshade.cache.set("bot_index", index, expiry=30)
        return index
    else:
        raise HTTPException(400, "Not yet implemented")

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

@app.get("/__docs/models")
async def get_models():
    return HTMLResponse(mapleshade.load_doc("models"))