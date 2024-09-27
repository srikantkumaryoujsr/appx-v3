
import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "758404034HXPvwIjmNpXoxz2toE")
    API_ID = int(os.environ.get("API_ID", "20654"))
    API_HASH = os.environ.get("API_HASH", "a10be717d1bc18303FT5448c6a7b0623849")
    AUTH_USERS = "765765787"


