from pathlib import Path

from environs import Env

env = Env()
env.read_env()

support_ids = list(map(int, env.list("SUPPORTS")))
BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = list(map(int, env.list("ADMINS")))
IP = env.str("IP")

DB_USER = env.str('DB_USER')
DB_PASS = env.str('DB_PASS')
DB_HOST = env.str('DB_HOST')
DB_NAME = env.str('DB_NAME')

SECRET_KEY = env.str("SECRET_KEY")

I18N_DOMAIN = "testbot"
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / "locales"

Yandex_API_KEY = env.str('API_KEY')
