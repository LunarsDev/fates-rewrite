import uuid
from fates import models
from fates.auth import auth
from . import tables
from . import tags
import inspect
import piccolo
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import ORJSONResponse
from piccolo.columns.combination import WhereRaw
from starlette.routing import Mount
from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder

from mapleshade import SilverNoData, Mapleshade
import silverpelt.types.types as silver_types

mapleshade = Mapleshade()


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
    description="""
For more documentation on our API, see https://github.com/LunarsDev/fates-rewrite#developer-docs

## General Terms

**Snippet:** A snippet is a basic core/common representation of any bot or server on the list.
    """,
)

@app.middleware("http")
async def cors(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Credentials"] = "false"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Content-Type, Authorization, Accept, Frostpaw-Cache, Frostpaw-Auth, Frostpaw-Target, Frostpaw-Server"

    if request.method == "OPTIONS":
        response.status_code = 200
    return response


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


@app.get("/random", response_model=models.Snippet, tags=[tags.bot])
async def random_snippet(
    target_type: models.TargetType = models.TargetType.Bot, reroll: bool = False
):
    """
Fetches a random 'snippet' from the list.

**Query Parameters**

- reroll: Whether to reroll and bypass cache (default: false)
    """
    if target_type == models.TargetType.User:
        raise HTTPException(400, detail="User snippets are not supported *yet*")
    if target_type != models.TargetType.Bot:
        return
    if not reroll:
        if cached := mapleshade.cache.get("random-bot"):
            return cached.value()
    flag = 0
    while flag < 10:
        try:
            v = (
                await mapleshade.to_snippet(
                    await models.augment(
                        tables.Bots.select(*models.BOT_SNIPPET_COLS).where(
                            tables.Bots.state == models.BotServerState.Certified
                        ),
                        "ORDER BY RANDOM() LIMIT 1",
                    )
                )
            )[0]
            mapleshade.cache.set("random-bot", v, expiry=60 * 60 * 3)
            return v
        except Exception as exc:
            print(exc)
            flag += 1


@app.get("/index", response_model=models.Index, tags=[tags.generic])
async def index(target_type: models.TargetType):
    if target_type != models.TargetType.Bot:
        raise HTTPException(400, "Not yet implemented")
    if cached_index := mapleshade.cache.get("bot_index"):
        return cached_index.value()
    index = models.Index(
        top_voted=await mapleshade.to_snippet(
            await tables.Bots.select(*models.BOT_SNIPPET_COLS)
            .where(tables.Bots.state == models.BotServerState.Approved)
            .order_by(tables.Bots.votes, ascending=False)
            .limit(12)
        ),
        new=await mapleshade.to_snippet(
            await tables.Bots.select(*models.BOT_SNIPPET_COLS)
            .where(tables.Bots.state == models.BotServerState.Approved)
            .order_by(tables.Bots.created_at, ascending=False)
            .limit(12)
        ),
        certified=await mapleshade.to_snippet(
            await tables.Bots.select(*models.BOT_SNIPPET_COLS)
            .where(tables.Bots.state == models.BotServerState.Certified)
            .order_by(tables.Bots.votes, ascending=False)
            .limit(12)
        ),
    )
    mapleshade.cache.set("bot_index", index, expiry=30)
    return index


@app.get("/bots/{bot_id}", tags=[tags.bot], response_model=models.Bot)
async def get_bot(bot_id: int):
    bot = await mapleshade.bot(bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Not Found")
    return bot

@app.get("/bots/{bot_id}/secrets", tags=[tags.bot], response_model=models.BotSecrets)
async def get_bot_secrets(bot_id: int, auth: models.AuthData = Depends(auth)):
    bot_owners = await tables.BotOwner.select().where(tables.BotOwner.bot_id == bot_id)

    if not bot_owners:
        raise HTTPException(status_code=404, detail="Not Found")
    
    flag = False
    for owner in bot_owners:
        if owner["owner"] == auth.target_id:
            flag = True
            break
    
    if not flag:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    bot_secrets = await tables.Bots.select(tables.Bots.webhook, tables.Bots.webhook_secret, tables.Bots.api_token).where(tables.Bots.bot_id == bot_id).first()

    return models.BotSecrets(
        api_token=bot_secrets["api_token"],
        webhook=bot_secrets["webhook"],
        webhook_secret=bot_secrets["webhook_secret"]
    )

@app.get("/@auth", tags=[tags.tests], response_model=models.AuthData)
async def test_auth(auth: models.AuthData = Depends(auth)):
    return auth

@app.get("/@me", tags=[tags.tests], response_model=silver_types.DiscordUser)
async def test_sv_resp():
    """Returns the current Fates List user thats logged in on the API"""
    req = await mapleshade.silverpelt_req("@me")
    return req


@app.get("/blazefire/{id}", tags=[tags.generic], response_model=silver_types.DiscordUser)
async def get_discord_user(id: int):
    try:
        req = await mapleshade.silverpelt_req(f"users/{id}")
    except SilverNoData as e:
        raise HTTPException(status_code=404, detail="Not Found") from e
    return req


@app.get("/meta", tags=[tags.generic], response_model=models.ListMeta)
async def get_meta():
    return models.ListMeta(
        bot=models.BotListMeta(
            tags=models.Tag.to_list(await tables.BotListTags.select()),
            features=models.Feature.to_list(await tables.Features.select()),
        ),
        server=models.ServerListMeta(
            tags=models.Tag.to_list(await tables.ServerTags.select()),
        ),
    )

@app.get("/code/{vanity}", tags=[tags.generic], response_model=models.Vanity)
async def get_code(vanity: str):
    vanity = await tables.Vanity.select().where(WhereRaw("lower(vanity_url) = {}", vanity.lower())).first()

    if not vanity:
        raise HTTPException(status_code=404, detail="Not Found")

    if vanity["type"] == 0:
        vanity["type"] = models.TargetType.Server
    elif vanity["type"] == 1:
        vanity["type"] = models.TargetType.Bot
    elif vanity["type"] == 2:
        vanity["type"] = models.TargetType.User
    else:
        raise HTTPException(status_code=400, detail="Unknown Vanity Type")
    
    return models.Vanity(
        target_type=vanity["type"],
        code=vanity["vanity_url"],
        target_id=vanity["redirect"]
    )

@app.get("/oauth2", tags=[tags.internal])
async def oauth2(request: Request):
    if not request.headers.get("Frostpaw-Server"):
        raise HTTPException(400, "Missing Frostpaw-Server header")
    state = str(uuid.uuid4())
    return {
        "state": state,
        "url": f"https://discord.com/oauth2/authorize?client_id={mapleshade.config['secrets']['client_id']}&redirect_uri={request.headers.get('Frostpaw-Server')}/frostpaw/login&scope=identify&response_type=code",
    }

@app.get("/guppy", tags=[tags.internal])
async def guppy_test(user_id: int):
    return await mapleshade.guppy(user_id)