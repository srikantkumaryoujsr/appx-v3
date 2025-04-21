
import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7955651454:AAEOwT7jKi1M9a4UhnQrjB-jJqVLkrVZ6C0")
    API_ID = int(os.environ.get("API_ID", "21832573"))
    API_HASH = os.environ.get("API_HASH", "aa2887b8dff6e44ba676cae70c2796f0")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://priyasingh92782:<db_password>@cluster0.bauky.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    AUTH_USERS = [7009468802, 7513565186, 7734031524, 6026885967]


