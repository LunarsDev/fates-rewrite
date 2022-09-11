VERSION = 1

import datetime
import secrets
import uuid
import asyncpg
import os
import asyncio
from fastapi.encoders import jsonable_encoder
import json

from typing import Any

os.environ["PGDATABASE"] = "fateslist"

print("Creating pg_dump")

os.system("rm -rf seedman/schema.sql seedman/seed_data.json")

code = os.system(f"pg_dump --verbose -Fc --schema-only --no-owner -d fateslist > seedman/schema.sql")

print("Exited with code", code)

class SeedSource():
    def __init__(self, table: str, column: str, value: Any):
        self.table = table
        self.column = column
        self.value = value

class TODO():
    def __init__(self, table: str):
        self.table = table

async def main():
    BOT_ID = "721279531939397673"

    SEED_PARENT = [
        SeedSource(table="users", column="user_id", value="563808552288780322"), # Rootsprings user info
        SeedSource(table="users", column="bot_id", value="728871946456137770"), # Burgerkings user info
        SeedSource(table="bots", column="bot_id", value="721279531939397673"), # Bristlefrost bot

        # Cant be seeded as theres no data to seed from
        TODO("reviews"), 
    ]

    conn = await asyncpg.connect() 

    seed_data = []

    for seed in SEED_PARENT:
        if isinstance(seed, TODO):
            continue
        # Fetch the seed data
        seed_data.append({
            "table": seed.table,
            "data": jsonable_encoder(await conn.fetch(f"SELECT * FROM {seed.table} WHERE {seed.column} = $1", seed.value))
        })

    cleaned_seed = []

    # Strip out api tokens from the data
    for seed in seed_data:
        seed_inf = {"table": seed["table"], "data": []}
        for row in seed["data"]:
            row_inf = {}
            for key, value in row.items():
                if key == "webhook":
                    row_inf[key] = "https://testhook.xyz"
                elif "token" in key or "secret" in key:
                    row_inf[key] = str(uuid.uuid4())
                else:
                    row_inf[key] = value
            seed_inf["data"].append(row_inf)
        cleaned_seed.append(seed_inf)

    # Write the seed data to a file
    with open("seedman/seed_data.json", "w") as f:
        json.dump(cleaned_seed, f)

    # Save seed versioning info in a file as well
    with open("seedman/seed_meta.json", "w") as f:
        json.dump({
            "nonce": secrets.token_urlsafe(16),
            "version": VERSION,
            "created_at": datetime.datetime.now().isoformat()
        }, f)

    # update this file to increment version
    with open("seedman/create_seed_files.py") as f:
        lines = f.readlines()
    
    lines[0] = f"VERSION = {VERSION + 1} # Auto-updated on {datetime.datetime.now()}\n"

    with open("seedman/create_seed_files.py", "w") as f:
        f.writelines(lines)

asyncio.run(main())
