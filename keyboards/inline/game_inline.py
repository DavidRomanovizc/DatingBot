from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def game_keyboard(is_premium: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    buy_nft = InlineKeyboardButton(text=_("💸 Приобрести подписку"), callback_data="pay_balance")
    back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="start_menu")
    choice_date = InlineKeyboardButton(text=_("🕕 Выберите дату"), callback_data="choice_the_date")
    if is_premium:
        markup.add(choice_date)
    else:
        markup.add(buy_nft)
    markup.add(back)
    return markup
