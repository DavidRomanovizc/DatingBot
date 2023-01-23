from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


async def language_keyboard(menu: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    ru = InlineKeyboardButton(text=_("🇷🇺 Русский"), callback_data="Russian")
    de = InlineKeyboardButton(text=_("🇩🇪 Немецкий"), callback_data="Deutsch")
    eng = InlineKeyboardButton(text=_("🇬🇧 Английский"), callback_data="English")
    ind = InlineKeyboardButton(text=_("🇮🇩 Индонезийский"), callback_data="Indonesian")

    if menu == "registration":
        back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="back_to_reg_menu")
        markup.row(ru, de)
        markup.row(eng, ind)
        markup.add(back)
        return markup
    elif menu == "profile":
        back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="back_to_profile_menu")
        markup.row(ru, de)
        markup.row(eng, ind)
        markup.add(back)
        return markup
