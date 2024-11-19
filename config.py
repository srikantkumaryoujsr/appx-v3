
import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7508390450:AAEp39kEUvmtwnmHhgZ2EO6QscIhG9hrRPE")
    API_ID = int(os.environ.get("API_ID", "20821267"))
    API_HASH = os.environ.get("API_HASH", "8723cdf433be176300044547ee6bab7a")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://aiitassam:SY06t3delyAShe71@cluster0.ugawa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    AUTH_USERS = [7224758848, 7513565186, 6804641253]


