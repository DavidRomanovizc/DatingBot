from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_inline_kb = InlineKeyboardMarkup(row_width=3,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='💬 Моя анекта',
                                                                   callback_data='my_profile')
                                          ],

                                          [
                                              InlineKeyboardButton(text='🧐 Смотреть анкеты',
                                                                   callback_data='find_ancets'),
                                              InlineKeyboardButton(text='⬆️ Изменить анкету',
                                                                   callback_data='change_profile')

                                          ],

                                          [
                                              InlineKeyboardButton(text='⏪️ Вернуться в меню',
                                                                   callback_data='start_menu')
                                          ],

                                      ]
                                      )
