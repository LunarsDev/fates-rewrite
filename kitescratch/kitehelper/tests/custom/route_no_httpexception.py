# Checks that no code in Fates List routes.py has HTTPException.
import os

# Check 1: routes.py containing any HTTPException
with open("fates/routes.py") as file:
    routes = file.read()

if "HTTPException" in routes:
    print("fates/routes.py contains illegal `HTTPException`")
    exit(1)

# Check 2: any file containing a ``raise HTTPException`` or a ``return HTTPException``
py_files = os.listdir("kitescratch/kitecli/api")

for py_file in py_files:
    with open(f"kitescratch/kitecli/api/{py_file}") as file:
        py_file_content = file.read()

    if "raise HTTPException" in py_file_content:
        print(f"kitescratch/kitecli/api/{py_file} contains illegal `raise HTTPException`")
        exit(1)

    if "return HTTPException" in py_file_content:
        print(f"kitescratch/kitecli/api/{py_file} contains illegal `return HTTPException`")
        exit(1)
