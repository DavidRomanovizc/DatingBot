from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

action_keyboard = CallbackData("questionnaire", "action")


async def questionnaires_keyboard():
    markup = InlineKeyboardMarkup(row_width=5)
    like = InlineKeyboardButton(text='👍', callback_data=action_keyboard.new(action="like"))
    dislike = InlineKeyboardButton(text='👎', callback_data=action_keyboard.new(action="dislike"))
    go_back = InlineKeyboardButton(text=f'⏪️ Остановить',
                                   callback_data=action_keyboard.new(action="stopped"))
    markup.row(like, dislike)
    markup.add(go_back)
    return markup


action_reciprocity_keyboard = CallbackData("questionnaire", "action")


async def reciprocity_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    like = InlineKeyboardButton(text='👍', callback_data=action_reciprocity_keyboard.new(action="like_reciprocity"))
    dislike = InlineKeyboardButton(text='👎',
                                   callback_data=action_reciprocity_keyboard.new(action="dislike_reciprocity"))
    markup.row(like, dislike)

    return markup


async def back_viewing_ques_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton(text='Вернуться к просмотру анкет', callback_data="go_back_to_viewing_ques")
    markup.row(back)

    return markup
