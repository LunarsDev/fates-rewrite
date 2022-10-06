# Checks requirements.txt first to get list of imports, then:
# - Checks all files in ``fates`` and ``silverpelt`` folders for imports not in requirements.txt

MODULES = (
    "fates",
    "silverpelt",
)

ALLOWED_UNUSED = (
    "uvicorn", # Used as a standalone server
)

import os
import sys

with open("requirements.txt") as file:
    requirements = file.readlines()

# Remove all comments
requirements = [line.replace("\n", "") for line in requirements if not line.startswith("#")]

# Handle aliases (could be done better but this works)
aliases = [line.split("alias-for=")[1].replace(" ", "") for line in requirements if "#!alias-for=" in line]
aliased = [line.split("#")[0].replace(" ", "") for line in requirements if "#!alias-for=" in line]

print("Aliases:", aliases)
print("Aliased:", aliased)

requirements += aliases

# Split out [ and # 
requirements = [line.split("[")[0].split("#")[0].replace(" ", "") for line in requirements]
special_imports = [v for v in requirements if "." in v]

print("Found requirements:", requirements)
print("[Special imports]:", special_imports)

def get_imports(file):
    with open(file) as file:
        content = file.read()

    imports = []

    content = [v.split("#")[0].replace('"', "'").replace("  ", "").replace("\t", "") for v in content.split("\n") if not v.startswith("#")]

    for line in content:
        if line.startswith("import "):
            imports.append(line.split(" ")[1])
        elif line.startswith("from "):
            imports.append(line.split(" ")[1])
        elif line.startswith("importlib.import_module"):
            imports.append(line.split("'")[1])
        elif line.startswith("__import__"):
            raise Exception(f"__import__ found in {file}. Please use import, from or importlib.import_module ONLY.")

    return imports

# Get all imports in fates and silverpelt
fates_imports = []

for module in MODULES:
    for root, dirs, files in os.walk(module):
        for file in files:
            if file.endswith(".py"):
                fates_imports += get_imports(os.path.join(root, file))
        
# It looks ugly but:
# -> If import in special_imports, it's fine to keep as-is
# -> Otherwise, we split the import by . and push
#    each part to the list of imports to check (fates_imports)
# -> Lastly, we remove duplicates after removing any empty elements and the modules itself
fates_imports = list(set([v for v in [(v.split(".")[0] if v not in special_imports else v) for v in fates_imports] if v and v not in MODULES]))
standard_imports = [v for v in fates_imports if v in sys.stdlib_module_names]

print("Found the following imports:")
print(fates_imports)

print("Standard imports:")
print(standard_imports)

# Remove standard imports
external_imports = [v for v in fates_imports if v not in standard_imports]

print("External imports:")
print(external_imports)

for external_import in external_imports:
    if external_import not in requirements:
        raise Exception(f"External import {external_import} not found in requirements.txt")

if external_import != requirements:
    to_remove = [v for v in requirements if v not in external_imports and v not in aliased and v not in ALLOWED_UNUSED]

    if to_remove:
        print("Requirements.txt contains more imports than the code. Please remove the following imports:")
        print(to_remove)
        exit(1)