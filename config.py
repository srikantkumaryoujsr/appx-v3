
import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7323888833:AAFJz-UpbqKLLcIn7h-lEklSBatdnmaBftE")
    API_ID = int(os.environ.get("API_ID", "22924674"))
    API_HASH = os.environ.get("API_HASH", "4490358fa3f47ba78643e02d14018083")
    AUTH_USERS = "6741261680"


