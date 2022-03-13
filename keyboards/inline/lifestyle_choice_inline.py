from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

lifestyle_inline_kb = InlineKeyboardMarkup(row_width=2,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text='Учусь',
                                                                        callback_data='study_lifestyle'),

                                                   InlineKeyboardButton(text='Работаю',
                                                                        callback_data='work_lifestyle')
                                               ],

                                               [
                                                   InlineKeyboardButton(text='Ищу работу',
                                                                        callback_data='job_find_lifestyle')
                                               ],
                                               [
                                                   InlineKeyboardButton(text='Домохозяйка/Домохозяин',
                                                                        callback_data='householder_lifestyle')
                                               ],

                                           ]
                                           )
