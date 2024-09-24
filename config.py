
import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7584040377:AAGiQBvX1nh-9NG64HXPvwIjmNpXoxz2toE")
    API_ID = int(os.environ.get("API_ID", "20863912"))
    API_HASH = os.environ.get("API_HASH", "a10be717d1bc18303a48c6a7b0623849")
    AUTH_USERS = "7513565186"


