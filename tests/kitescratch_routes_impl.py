import pathlib
import sys
sys.path.append(".")

# Fates routes needs the event loop to work
import asyncio

async def _start_eloop():
    from fates import routes as _

asyncio.run(_start_eloop())

from fates import decorators

go_files = {}

for f in pathlib.Path().rglob("kitescratch/api/*.go"):
    with open(f, "r") as file:
        go_files[f.name] = file.read()

for name, route in decorators.routes.items():
    if len(route.route.tags) > 1:
        raise Exception(f"Route {name} MUST only have one tag")
    print(name, route.route.tags)