# Simple test to ensure enums.py does *not* contain pydantic whatsoever. Such code is for models.py

with open("libcommon/enums.py") as file:
    enums = file.read()

if "pydantic" in enums:
    print("libcommon/enums.py contains illegal `pydantic`. Move it to models.py")
    exit(1)

if "BaseModel" in enums:
    print("libcommon/enums.py contains illegal `BaseModel` from pydantic. Move it to models.py")
    exit(1)