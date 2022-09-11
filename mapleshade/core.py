from fates import tables, models
from ruamel.yaml import YAML

class Mapleshade():
    __slots__=['yaml', 'config']
    def __init__(self):
        self.yaml = YAML()

        with open("config.yaml") as doc:
            self.config = self.yaml.load(doc)

    async def bot(self, bot_id: int) -> models.Bot:
        """Returns a bot from the database"""
        bot = await tables.Bots.select().where(tables.Bots.id == bot_id).first()

        return models.Bot(**bot)
    
    async def user(self, user_id: int) -> models.User:
        """Returns a user from the database"""
        user = await tables.Users.select().where(tables.Users.id == user_id).first()

        return models.User(**user)