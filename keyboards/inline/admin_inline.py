from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

banned_user = CallbackData("questionnaire", "action")


async def admin_mode_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    mailing_button = InlineKeyboardButton('Провести рассылку', callback_data='mailing_start')
    count_user_button = InlineKeyboardButton('Просмотреть количество пользователей', callback_data='show_active_users')
    ban_user_button = InlineKeyboardButton('Забанить юзер id 🛑', callback_data='ban_user_id')
    find_user_button = InlineKeyboardButton('Найти пользователя', callback_data='find_users')
    give_admin_button = InlineKeyboardButton('Выдать админку', callback_data='give_admin')
    site_admin_button = InlineKeyboardButton('Сайт-админка🛑', callback_data='admin_site_url')
    markup.add(give_admin_button, count_user_button, ban_user_button, find_user_button, mailing_button,
               site_admin_button)
    return markup


async def banned_user_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    ban_user_button = InlineKeyboardButton('Забанить', callback_data=banned_user.new(action='ban_user'))
    not_bun_button = InlineKeyboardButton('Не банить', callback_data=banned_user.new(action='not_ban_user'))
    markup.add(ban_user_button, not_bun_button)
    return markup


async def approval_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    mailing_button = InlineKeyboardButton('Провести рассылку', callback_data='approved_btn')
    markup.add(mailing_button)
    return markup


async def find_user_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    found_id_user_button = InlineKeyboardButton("Искать по ID", callback_data="find_id")
    found_name_user_button = InlineKeyboardButton("Искать по имени", callback_data="find_user")
    markup.add(found_id_user_button, found_name_user_button)
    return markup
