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

for f in pathlib.Path().rglob("kitescratch/kitecli/api/*.go"):
    with open(f) as file:
        go_files[f.name.replace(".go", "")] = file.read()

with open("kitescratch/kitecli/views.go") as file:
    go_files["views.go"] = file.read()

for name, route in decorators.routes.items():
    if route.route.tags[0].name == "tests":
        continue
    if route.route.tags[0].name not in go_files.keys():
        print(f"Missing tag {route.route.tags[0].name} in kitescratch/kitecli/api")
        exit(1)

    if name.replace("_", " ").title().replace(" ", "") not in go_files[route.route.tags[0].name]:
        print(f"Missing route {name} in kitescratch/kitecli/api/{route.route.tags[0].name}.go")
        exit(1)
    
    if name.replace("_", " ").title().replace(" ", "") not in go_files["views.go"]:
        print(f"Missing route {name} in kitescratch/kitecli/views.go")
        exit(1)