
import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "a10be717d1bc18303a48c6a7b0623849")
    API_ID = int(os.environ.get("API_ID", "20863912"))
    API_HASH = os.environ.get("API_HASH", "68e0b4f357cd483d4b891ac6bf0e7e6a")
    AUTH_USERS = "7513565186"


