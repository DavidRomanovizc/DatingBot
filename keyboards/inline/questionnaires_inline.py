from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

questionnaires_inline_kb = InlineKeyboardMarkup(row_width=4,
                                                inline_keyboard=[
                                                    [
                                                        InlineKeyboardButton(text='Лайк',
                                                                             callback_data='like_questionnaire'),
                                                        InlineKeyboardButton(text='Дизлайк',
                                                                             callback_data='dislike_questionnaire'),
                                                        InlineKeyboardButton(text='Отправить сообщение',
                                                                             callback_data='send_message_questionnaire'),
                                                        InlineKeyboardButton(text='Пожаловаться',
                                                                             callback_data='report'),

                                                    ]]
                                                )