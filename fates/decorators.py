import datetime
from functools import wraps
import traceback
from typing import Awaitable, Any, Literal, Optional, Protocol, Type, TypeVar, get_origin
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.params import Depends as DependsType
from enum import IntEnum
from pydantic import BaseModel, validator
from inspect import signature
from fates import models, consts
from fates.mapleshade import Mapleshade
import base64
import orjson
import asyncpg

from fates.tags import Tag


class Method(IntEnum):
    get = 0
    post = 1
    put = 2
    patch = 3
    delete = 5
    head = 6


class Ratelimit(BaseModel):
    num: int
    """Number of requests"""

    interval: int | float
    """Time interval (seconds)"""

    name: str
    """The name of the ratelimit (the rl will apply to all ratelimits with said name)"""


class SharedRatelimit:
    _shared_rls = {
        "core": Ratelimit(
            num=200,  # Avoid ratelimiting core endpoints as far as possible
            interval=1,
            name="core",
        )
    }

    @staticmethod
    def new(name: str) -> "Ratelimit":
        return SharedRatelimit._shared_rls[name]


class Route(BaseModel):
    app: FastAPI
    mapleshade: Mapleshade
    url: str
    response_model: Any
    method: Method
    tags: list[Tag]
    ratelimit: Ratelimit  # We don't actually ratelimit yet, this is for forwards-compat
    auth: Optional[
        models.TargetType | bool
    ] = None  # Either None, a target type or true (for all)

    class Config:
        arbitrary_types_allowed = True

    @validator("tags")
    def tag_length(cls, v):
        if len(v) > 1:
            raise ValueError("A route can only have 1 tags")
        return v


class __RouteData:
    """Internal class for handling routes"""

    def __init__(self, func: Awaitable, route: Route):
        self.func: Awaitable = func
        self.route: Route = route

    def get_tio_type(self, v: Any) -> str:
        tio_types = {
            str: "text",
            int: "number",
            bool: "bool",
            datetime.datetime: "datetime-local",
            list[str]: "list:number",
            list[int]: "list:text",
        }

        return tio_types.get(v) or "text"

    def extract_bm(self, bm: BaseModel) -> dict[str, Any]:
        """Extracts the fields from a BaseModel"""
        fields = {}

        for field in bm.__fields__.values():
            if get_origin(field.type_) is Literal: # If it is a literal
                fields[field.name] = "text"
            elif issubclass(field.type_, BaseModel):
                fields[field.name] = {"_nested": True} | self.extract_bm(
                    field.annotation
                )
                continue
            fields[field.name] = self.get_tio_type(field.annotation)

        return fields

    def extract_tryitout(self) -> dict[str, Any]:
        """Extracts the tryitout data (query params, path params, body, headers) from the function"""
        tryitout = {
            "name": self.func.__name__,
            "query": {},
            "path": {},
            "body": {},
            "auth": [v.name for v in models.TargetType]
            if self.route.auth == True
            else [self.route.auth.name]
            if self.route.auth
            else [],
        }

        sig = signature(self.func)

        # Get all the path params for route.url
        path_params = [
            v[1:-1].split(":")[0]
            for v in self.route.url.split("/")
            if v.startswith("{") and v.endswith("}")
        ]

        # Handle path params
        for param in path_params:
            if param in sig.parameters:
                tryitout["path"][param] = self.get_tio_type(
                    sig.parameters[param].annotation
                )

        # First find the body param
        for key, param in sig.parameters.items():

            # Body param
            if issubclass(param.annotation, BaseModel):
                # Check that it is not a dependency
                if issubclass(type(param.default), DependsType):
                    continue

                # Loop over all fields of the base model
                tryitout["body"] = self.extract_bm(param.annotation)

            else:
                # Query param or path param
                if key in path_params or key == "request":
                    continue

                tryitout["query"][key] = self.get_tio_type(param.annotation)

        return tryitout


T = TypeVar("T", covariant=True)


class __RouteProtocol(Protocol[T]):
    """Type hints for a route"""

    def __init__(
        self,
        path: str,
        responses: dict[int, Any],
        response_model: Any = None,
        tags: list[str] = None,
        operation_id: str = None,
    ) -> None:
        ...


routes = {}


def route(route: Route):
    def rw(func: Awaitable):
        if not func.__doc__:
            raise ValueError("Function must have a docstring")

        if func.__name__ in routes:
            raise ValueError("Function name must be unique")

        route_data = __RouteData(func, route)

        routes[func.__name__] = route_data

        try_data = orjson.dumps(route_data.extract_tryitout())

        func.__doc__ += f"""

<div id="{func.__name__}" class="try-it-out" data-tryitout="{base64.urlsafe_b64encode(try_data).decode()}">
    """

        rmap: dict[Method, Type[__RouteProtocol]] = {
            Method.get: route.app.get,
            Method.post: route.app.post,
            Method.put: route.app.put,
            Method.patch: route.app.patch,
            Method.delete: route.app.delete,
            Method.head: route.app.head,
        }

        # Check the args of func
        func_sig = signature(func)

        if not func_sig.parameters.get("request"):
            raise ValueError("Function must take request")

        @wraps(func)
        async def custom_route(request: Request, *args, **kwargs):
            try:
                res = await func(request, *args, **kwargs)
            except HTTPException as e:
                return ORJSONResponse(
                    models.Response(
                        done=False,
                        reason=e.detail,
                        code=consts.DEFAULT_EXC.get(
                            e.status_code, models.ResponseCode.UNKNOWN
                        ),
                    ).dict(),
                    status_code=e.status_code,
                )
            except models.ResponseRaise as e:
                return ORJSONResponse(e.response.dict(), status_code=e.status_code)
            except asyncpg.exceptions.DataError as e:
                return ORJSONResponse(
                    models.Response(
                        done=False,
                        reason=str(e),
                        code=models.ResponseCode.INVALID_DATA,
                    ).dict(),
                    status_code=400,
                )
            except Exception as e:
                traceback.print_exc()
                return ORJSONResponse(
                    models.Response(
                        done=False,
                        reason=repr(e),
                        code=models.ResponseCode.INTERNAL_ERROR,
                    ).dict(),
                    status_code=500,
                )

            return res

        if route.response_model == Any:
            route.response_model = None

        rmap[route.method](
            route.url,
            response_model=route.response_model,
            tags=[tag.fname for tag in route.tags],
            operation_id=func.__name__,
            responses={
                404: {"model": models.Response},
                400: {"model": models.Response},
                409: {"description": "Not Implemented", "model": models.Response},
                500: {"description": "Something Went Wrong", "model": models.Response},
            },
        )(custom_route)

    return rw


def nop(*_):
    """NOP (unused request can use this)"""
    ...
