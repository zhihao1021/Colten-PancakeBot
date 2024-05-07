from orjson import dumps, loads, OPT_INDENT_2
from pydantic import BaseModel

from os import urandom
from os.path import isfile
from traceback import print_exc


class MongoDBConfig(BaseModel):
    db_url: str = ""
    db_name: str = ""


class DiscordBotConfig(BaseModel):
    token: str = ""
    managers: list[int] = []
    guard_id: int = 0
    main_channel: int = 0
    stock_channel: int = 0
    embed_footer_text: str = ""
    embed_footer_image: str = ""
    stock_change_image: str = ""
    stock_change_thumbnail: str = ""


class APIConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class OAuthConfig(BaseModel):
    jwt_key: str = urandom(16).hex()
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = ""


class Config(BaseModel):
    mongo_db: MongoDBConfig = MongoDBConfig()
    discord_bot: DiscordBotConfig = DiscordBotConfig()
    api: APIConfig = APIConfig()
    oauth: OAuthConfig = OAuthConfig()


if isfile("config.json"):
    try:
        with open("config.json", "rb") as config_file:
            content = config_file.read()
            with open("config.bak.json", "wb") as backup_config_file:
                backup_config_file.write(content)
            config = Config(**loads(content))
    except:
        print_exc()
        print("Read config.json failed, please check your config file")
        exit(0)
else:
    config = Config()

with open("config.json", "wb") as config_file:
    config_file.write(dumps(
        config.model_dump(),
        option=OPT_INDENT_2
    ))


DB_URL = config.mongo_db.db_url
DB_NAME = config.mongo_db.db_name

BOT_TOKEN = config.discord_bot.token
BOT_MANAGERS = config.discord_bot.managers
BOT_GUARD_ID = config.discord_bot.guard_id
BOT_MAIN_CHANNEL = config.discord_bot.main_channel
BOT_STOCK_CHANNEL = config.discord_bot.stock_channel
BOT_EMBED_FOOTER_TEXT = config.discord_bot.embed_footer_text
BOT_EMBED_FOOTER_IMAGE = config.discord_bot.embed_footer_image
BOT_STOCK_CHANGE_IMAGE = config.discord_bot.stock_change_image
BOT_STOCK_CHANGE_THUMBNIAL = config.discord_bot.stock_change_thumbnail

API_HOST = config.api.host
API_PORT = config.api.port

OAUTH_JWT_KEY = config.oauth.jwt_key
OAUTH_CLIENT_ID = config.oauth.client_id
OAUTH_CLIENT_SECRET = config.oauth.client_secret
OAUTH_REDIRECT_URI = config.oauth.redirect_uri

_map_data = {
    "Mongo DB URL": DB_URL,
    "Mongo DB table name": DB_NAME,
    "Discord bot token": BOT_TOKEN,
    "Guard user id": BOT_GUARD_ID,
    "Discord main channel id": BOT_MAIN_CHANNEL,
    "Discord stock channel id": BOT_STOCK_CHANNEL,
    "API host": API_HOST,
    "API port": API_PORT,
    "Discord oauth JWT key": OAUTH_JWT_KEY,
    "Discord oauth client id": OAUTH_CLIENT_ID,
    "Discord oauth client secret": OAUTH_CLIENT_SECRET,
    "Discord oauth redirect uri": OAUTH_REDIRECT_URI,
}

check_success = True
for key, value in _map_data.items():
    if not value:
        check_success = False
        print(f"Config Error: {key} is missing.")
if check_success:
    print("Config check success")
else:
    print("Config check failed, please go to modify your config.json")
    exit(0)
