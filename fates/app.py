import hashlib
import hmac
import time
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

from mapleshade import SilverNoData, Mapleshade, Permission
import silverpelt.types.types as silver_types
import orjson

mapleshade = Mapleshade()


_tables = []

tables_dict = vars(tables)

for obj in tables_dict.values():
    if obj == tables.Table:
        continue
    if inspect.isclass(obj) and isinstance(obj, piccolo.table.TableMetaclass):
        _tables.append(obj)

# Load all docs
docs = []
with open("docs/meta.json") as meta_f:
    meta: list[str] = orjson.loads(meta_f.read())

for file_name in meta:
    with open(f"docs/{file_name}") as doc:
        docs.append(doc.read())

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
    docs_url=None,
    description="\n\n".join(docs),
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

@app.get("/bots/{bot_id}/invite", tags=[tags.bot], response_model=models.Invite)
async def get_bot_invite(request: Request, bot_id: int):
    """
    Gets the invite for a bot.

    If ``Frostpaw-Target`` is set to ``invite``, then this also updates invite_amount
    """
    invite_url = await tables.Bots.select(tables.Bots.invite).where(tables.Bots.bot_id == bot_id).first()

    if not invite_url:
        raise HTTPException(status_code=404, detail="Not Found")
    
    if request.headers.get("Frostpaw-Target") == "invite":
        await tables.Bots.update(invite_amount = tables.Bots.invite_amount + 1).where(tables.Bots.bot_id == bot_id)

    if not invite_url["invite"]:
        return models.Invite(
            invite=f"https://discord.com/api/oauth2/authorize?client_id={bot_id}&permissions=0&scope=bot%20applications.commands"
        )
    elif invite_url["invite"].startswith("P:"):
        perm_num = invite_url["invite"][2:]
        return models.Invite(
            invite=f"https://discord.com/api/oauth2/authorize?client_id={bot_id}&permissions={perm_num}&scope=bot%20applications.commands"
        )
    else:
        return models.Invite(invite=invite_url["invite"])

@app.get("/bots/{bot_id}/secrets", tags=[tags.bot], response_model=models.BotSecrets)
async def get_bot_secrets(bot_id: int, auth: models.AuthData = Depends(auth)):
    if auth.auth_type != models.TargetType.User:
        raise HTTPException(401, "User-only endpoint")

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

    vanity_map = {
        0: models.TargetType.Server,
        1: models.TargetType.Bot,
        2: models.TargetType.User,
    }

    try:
        vanity["type"] = vanity_map[vanity["type"]]
    except KeyError:
        raise HTTPException(status_code=500, detail="Unknown Vanity Type")
    
    return models.Vanity(
        target_type=vanity["type"],
        code=vanity["vanity_url"],
        target_id=vanity["redirect"]
    )

@app.get("/oauth2", tags=[tags.internal], response_model=models.OAuth2Login)
async def get_oauth2(request: Request):
    if not request.headers.get("Frostpaw-Server"):
        raise HTTPException(400, "Missing Frostpaw-Server header")
    state = str(uuid.uuid4())
    return {
        "state": state,
        "url": f"https://discord.com/oauth2/authorize?client_id={mapleshade.config['secrets']['client_id']}&redirect_uri={request.headers.get('Frostpaw-Server')}/frostpaw/login&scope=identify&response_type=code",
    }

@app.post("/oauth2", tags=[tags.internal], response_model=models.OauthUser)
async def login_user(request: Request, login: models.Login):
    redirect_url_d = request.headers.get("Frostpaw-Server")

    if not redirect_url_d:
        redirect_url_d = "https://fateslist.xyz"

    redirect_url = f'https://{redirect_url_d.replace("https://", "", 1).replace("http://", "", 1)}/frostpaw/login'

    if redirect_url_d.startswith("http://"):
        redirect_url = f'http://{redirect_url_d.replace("https://", "", 1).replace("http://", "", 1)}/frostpaw/login'

    try:
        oauth = await mapleshade.login(login.code, redirect_url)
    except Exception as e:
        print("Error logging in user", type(e), e)
        raise HTTPException(status_code=400, detail=str(e))
    
    return oauth

@app.get("/guppy", tags=[tags.internal], response_model=Permission)
async def guppy_test(user_id: int):
    return await mapleshade.guppy(user_id)