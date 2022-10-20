from ruamel.yaml import YAML
from typing import Any

yaml = YAML()

with open("config.yaml") as f:
    config: dict[str, Any] = yaml.load(f)
