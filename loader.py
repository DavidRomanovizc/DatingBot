from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from middlewares.language_middleware import setup_middleware
from utils.YandexMap.work_with_location import Client

from utils.db_api.postgres import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
# Configure i18n middleware to work with multilingualism
i18n = setup_middleware(dp)
# Creating an alias for the gettext method
_ = i18n.gettext
client = Client(api_key=config.Yandex_API_KEY)
