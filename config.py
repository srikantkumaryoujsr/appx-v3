
import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7352648570:AAEznBJFLrIEJHCsDIdxkoQqPu-hsTkNbms")
    API_ID = int(os.environ.get("API_ID", "20821267"))
    API_HASH = os.environ.get("API_HASH", "8723cdf433be176300044547ee6bab7a")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://srikantkumar2025:QC5M1BgTGxxUqM4R@cluster0.u6zhg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    AUTH_USERS = [7009468802, 7513565186, 7734031524, 7653322737]


