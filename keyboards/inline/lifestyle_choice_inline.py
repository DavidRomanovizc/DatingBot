from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def lifestyle_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    student = InlineKeyboardButton(text='Учусь', callback_data='study_lifestyle')
    working = InlineKeyboardButton(text='Работаю', callback_data='work_lifestyle')
    find_work = InlineKeyboardButton(text='Ищу работу', callback_data='job_find_lifestyle')
    housewife = InlineKeyboardButton(text='Домохозяйка/Домохозяин', callback_data='householder_lifestyle')
    markup.row(student, working)
    markup.add(find_work)
    markup.row(housewife)
    return markup
