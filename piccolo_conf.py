from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine
import os

# Load config.yaml
from ruamel.yaml import YAML

with open("config.yaml") as f:
    config = YAML().load(f)["storage"]["postgres"]

piccolo_cfg = {}

def get_opt(key: str, default_env: str):
    if config.get(key):
        piccolo_cfg[key] = config[key]
    elif os.getenv(default_env):
        piccolo_cfg[key] = os.getenv(default_env)
    
    print(f"Got {key}:", piccolo_cfg.get(key))

get_opt("host", "PGHOST")
get_opt("port", "PGPORT")
get_opt("user", "PGUSER")
get_opt("password", "PGPASSWORD")
get_opt("database", "PGDATABASE")

if not piccolo_cfg.get("database"):
    print("No database specified in config.yaml or environment variables")
    exit(1)

DB = PostgresEngine(config=piccolo_cfg)


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(apps=["fates.piccolo_app"])
