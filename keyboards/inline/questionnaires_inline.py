from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

action_keyboard = CallbackData("questionnaire", "action")


async def questionnaires_keyboard():
    markup = InlineKeyboardMarkup(row_width=5)
    like = InlineKeyboardButton(text='👍', callback_data=action_keyboard.new(action="like"))
    dislike = InlineKeyboardButton(text='👎', callback_data=action_keyboard.new(action="dislike"))
    go_back = InlineKeyboardButton(text=f'⏪️ Я больше не хочу никого искать',
                                   callback_data=action_keyboard.new(action="stopped"))
    markup.row(like, dislike)
    markup.add(go_back)
    return markup
