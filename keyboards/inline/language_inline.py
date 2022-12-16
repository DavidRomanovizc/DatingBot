from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def language_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    ru = InlineKeyboardButton(text=_("🇷🇺 Русский"), callback_data="Russian")
    de = InlineKeyboardButton(text=_("🇩🇪 Немецкий"), callback_data="Deutsch")
    eng = InlineKeyboardButton(text=_("🇬🇧 Английский"), callback_data="English")
    ind = InlineKeyboardButton(text=_("🇮🇩 Индонезийский"), callback_data="Indonesian")
    markup.add(ru, de)
    markup.add(eng, ind)
    return markup
