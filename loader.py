from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import load_config
from utils.YandexMap.api import Client

from utils.db_api.postgres import Database

bot = Bot(token=load_config().tg_bot.token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
client = Client(api_key=load_config().misc.yandex_api_key)
# scheduler = await aiojobs.create_scheduler()
