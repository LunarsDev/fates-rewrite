import enum
from fates import models
from fates import tags
from fates.decorators import nop
from libcommon import enums, tables
import inspect
import piccolo
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import ORJSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.routing import Mount
from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder
from fastapi.encoders import jsonable_encoder

from fates.mapleshade import Mapleshade

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
with open("docs/meta.yaml") as meta_f:
    meta: list[str] = mapleshade.yaml.load(meta_f)

for file_name in meta:
    with open(f"docs/{file_name}") as doc:
        docs.append(
            doc.read()
            .replace("{%sunbeam%}", mapleshade.config["deploy"]["sunbeam"])
            .replace("{%clientId%}", str(mapleshade.config["secrets"]["client_id"]))
        )

with open("docs/__docs_page.html") as dp:
    docs_page = (
        dp.read()
        .replace("{%sunbeam%}", mapleshade.config["deploy"]["sunbeam"])
        .replace("{%clientId%}", str(mapleshade.config["secrets"]["client_id"]))
    )

# Get enums
def document_enums():
    """Converts the enums into markdown for api docs"""
    md = {}

    for key in enums.__dict__.keys():
        # Ignore internal or dunder keys
        if key.startswith("_") or key in ("IntEnum", "Enum"):
            continue

        v = enums.__dict__[key]

        if not issubclass(v, enum.IntEnum) and not issubclass(v, enum.Enum):
            raise TypeError(f"Expected enum, got {type(v)} instead ({key})")

        props = list(v)

        try:
            fields = v.docs()

            if not fields:
                fields = {p.name: {} for p in props}

        except AttributeError:
            fields = {p.name: {} for p in props}

        md[key] = {}
        md[key]["doc"] = "\n"
        md[key]["table"] = "| Name | Value |"
        nl = "\n| :--- | :--- |"

        keys = []

        for ext in fields[list(fields.keys())[0]].keys():
            md[key]["table"] += f" {ext.strip('_').replace('_', ' ').title()} |"
            nl += " :--- |"
            keys.append(ext)

        md[key]["table"] += f"{nl}\n"

        if v.__doc__ and v.__doc__ != "An enumeration.":
            md[key]["doc"] = "\n" + v.__doc__ + "\n\n"

        for prop in props:
            md[key]["table"] += f"| {prop.name} | {prop.value} |"

            documented_prop = fields.get(prop.name, {})

            for prop_key in keys:
                tmp = documented_prop.get(prop_key, "")
                if not tmp:
                    raise ValueError(f"Missing {prop_key} for {prop.name} in {key}")

                md[key]["table"] += f" {tmp} |"

            md[key]["table"] += "\n"

    md = dict(sorted(md.items()))

    md_out = []

    for key in md.keys():
        md_out.append(f'### {key}\n{md[key]["doc"]}{md[key]["table"]}')

    return "## Enums\n" + "\n\n".join(md_out)


docs.append(document_enums())

app = FastAPI(
    title="Fates List",
    default_response_class=ORJSONResponse,
    openapi_tags=tags.tags_metadata,
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
    redoc_url=None,
    description="\n\n".join(docs),
)


@app.exception_handler(404)
async def not_found(_: Request, exc: HTTPException):
    """Handle 404 with a normalised error response"""
    return ORJSONResponse(
        models.Response(
            done=False,
            reason=exc.detail,
            code=models.DEFAULT_EXC.get(exc.status_code, models.ResponseCode.UNKNOWN),
        ).dict(),
        status_code=exc.status_code,
    )


@app.exception_handler(models.ResponseRaise)
async def response_raise_handler(_: Request, exc: models.ResponseRaise):
    """Handles ResponseRaise exceptions"""
    return ORJSONResponse(
        status_code=exc.status_code,
        content=exc.response.dict(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    """Handles validation error handling for normalizing errors"""
    return ORJSONResponse(
        status_code=422,
        content=models.Response(
            done=False,
            reason=str(exc),
            data=jsonable_encoder({"errors": exc.errors(), "body": exc.body}),
            code=models.ResponseCode.INVALID_DATA,
            errors=exc.errors(),
        ).dict(),
    )


@app.middleware("http")
async def cors(request: Request, call_next):
    """Add CORS headers to all responses."""
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
    """
    Opens the database connection pool and saves the pool in mapleshade for use in the rest of the app

    TODO: look into a better way to do this
    """

    engine = engine_finder()
    # asyncio.create_task(bot.start(secrets["token"]))
    # await bot.load_extension("jishaku")
    await engine.start_connnection_pool()

    mapleshade.pool = engine.pool


@app.on_event("shutdown")
async def close_database_connection_pool():
    """Closes the database connection pool"""
    engine = engine_finder()
    await engine.close_connnection_pool()


# This is the only exception to not using @route
@app.get("/docs", include_in_schema=False)
async def docs():
    """Returns the docs HTML"""
    return HTMLResponse(docs_page)


# Load all routes
from fates import routes, ws

nop(routes, ws)
