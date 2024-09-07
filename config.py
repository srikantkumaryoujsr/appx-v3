
import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7281731729:AAEgevvGlRs-URJI3FJ0DhwLTOypILbQdP4")
    API_ID = int(os.environ.get("API_ID", "27072814"))
    API_HASH = os.environ.get("API_HASH", "68e0b4f357cd483d4b891ac6bf0e7e6a")
    AUTH_USERS = "7513565186"


