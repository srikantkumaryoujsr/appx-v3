
import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7103819451:AAFp02pmf0FQjtcaP1phUTm4YPFGwt0IzwY")
    API_ID = int(os.environ.get("API_ID", "29581994"))
    API_HASH = os.environ.get("API_HASH", "367790bb9fd78d2a07a23ef9a654eb48")
    AUTH_USERS = "6748451207"


