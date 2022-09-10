from fates import tables
from ruamel.yaml import YAML

class Mapleshade():
    __slots__=['yaml', 'config']
    def __init__(self):
        self.yaml = YAML()

        with open("config.yaml") as doc:
            self.config = self.yaml.load(doc)
