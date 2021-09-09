from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_mode_kb = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton('Провести рассылку',
                                                                  callback_data='mailing_start'),
                                             InlineKeyboardButton('Создать базу пользователей',
                                                                  callback_data='create_base_users'),
                                             InlineKeyboardButton('Создать базу платежей',
                                                                  callback_data='create_base_Payments')
                                         ],
                                         [
                                             InlineKeyboardButton('Просмотреть количество юзеров',
                                                                  callback_data='show_active_users')
                                         ],
                                         [
                                             InlineKeyboardButton('Забанить юзер id🛑',
                                                                  callback_data='ban_user_id'),
                                             InlineKeyboardButton('Найти пользователя',
                                                                  callback_data='find_user')
                                         ],
                                         [
                                             InlineKeyboardButton('Выдать админку юзеру(only CEO/CTO)🛑',
                                                                  callback_data='give_admin'),

                                         ],
                                         [
                                             InlineKeyboardButton('Удалить пользователей из базы🛑',
                                                                  callback_data='delete_users_from_db'),
                                             InlineKeyboardButton('Инициализация пользователя(тест)',
                                                                  callback_data='initialization_user')
                                         ],
                                         [
                                             InlineKeyboardButton('Сайт-админка🛑',
                                                                  callback_data='admin_site_url')
                                         ],
                                         [
                                             InlineKeyboardButton('УДАЛИТЬ ВСЮ БАЗУ(only CEO/CTO)',
                                                                  callback_data='delete_db')
                                         ]
                                     ])
