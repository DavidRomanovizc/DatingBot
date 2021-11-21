from pathlib import Path
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

DB_USER = env.str('DB_USER')  # Имя пользователя db
DB_PASS = env.str('DB_PASS')  # Пароль от db
DB_HOST = env.str('DB_HOST')
DB_NAME = env.str('DB_NAME')  # Название db

I18N_DOMAIN = "testbot"
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / "locales"  # тут хранятся переводы

# Переменные для ЮKassa
UTOKEN = env.str("yootoken")

# Новые переменные для библиотеки QiwiApi
QIWI_TOKEN = env.str("qiwi")
WALLET_QIWI = env.str("wallet")  # номер телефона
QIWI_PUBKEY = env.str("qiwi_p_pub")  # Публичный ключ для генерации ссылки на оплаты
