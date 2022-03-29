from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def report_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    content = InlineKeyboardButton(text='🔞', callback_data='content')
    drug = InlineKeyboardButton(text='💊', callback_data='drugs')
    scam = InlineKeyboardButton(text='💰', callback_data='scam')
    another = InlineKeyboardButton(text='🦨', callback_data='another')
    cancel = InlineKeyboardButton(text='❌', callback_data='cancel_report')
    markup.add(content)
    markup.row(scam, drug, another)
    markup.add(cancel)
    return markup
