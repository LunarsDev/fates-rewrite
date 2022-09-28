from functools import wraps
from typing import Awaitable, Any
from fastapi import FastAPI, Request
from enum import IntEnum
from pydantic import BaseModel
from inspect import signature
from mapleshade import Mapleshade

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

class SharedRatelimit():
    _shared_rls = {
        "core": Ratelimit(
            num=200, # Avoid ratelimiting core endpoints as far as possible 
            interval=1,
            name="core"
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
    tags: list[str]
    ratelimit: Ratelimit # We don't actually ratelimit yet, this is for forwards-compat

    class Config:
        arbitrary_types_allowed = True



class __RouteData:
    """Internal class for handling routes"""

    def __init__(self, func: Awaitable):
        self.func: Awaitable = func


routes = {}

def route(route: Route):
    def rw(func: Awaitable):
        if not func.__doc__:
            raise ValueError("Function must have a docstring")

        if func.__name__ in routes:
            raise ValueError("Function name must be unique")
        
        routes[func.__name__] = __RouteData(func)

        func.__doc__ += f"""

<iframe style="width: 100%!important;" frameborder="0" src="{route.mapleshade.config['static']}/tryitout.html?name={func.__name__}"></iframe>
    """

        rmap = {
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
            return await func(request, *args, **kwargs)

        rmap[route.method](route.url, response_model=route.response_model, tags=route.tags)(custom_route)

    return rw

def nop(*_):
    """NOP (unused request can use this)"""
    ...