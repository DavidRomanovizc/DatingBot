from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def questionnaires_keyboard():
    markup = InlineKeyboardMarkup(row_width=5)
    like = InlineKeyboardButton(text=f"👍", callback_data='like_questionnaire')
    dislike = InlineKeyboardButton(text='👎', callback_data='dislike_questionnaire')
    send_msg = InlineKeyboardButton(text='💌', callback_data='send_message_questionnaire')
    send_report = InlineKeyboardButton(text='🛑', callback_data='send_report')
    go_back = InlineKeyboardButton(text=f'⏪️ Я больше не хочу никого искать', callback_data='stop_finding')
    markup.row(like, dislike)
    markup.row(send_msg, send_report)
    markup.add(go_back)
    return markup
