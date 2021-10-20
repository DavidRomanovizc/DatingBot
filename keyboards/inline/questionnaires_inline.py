from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

questionnaires_inline_kb = InlineKeyboardMarkup(row_width=5,
                                                inline_keyboard=[
                                                    [
                                                        InlineKeyboardButton(text=f"👍",
                                                                             callback_data='like_questionnaire'),
                                                        InlineKeyboardButton(text='👎',
                                                                             callback_data='dislike_questionnaire'),

                                                    ],
                                                    [
                                                        InlineKeyboardButton(text='💌',
                                                                             callback_data='send_message_questionnaire'),
                                                        InlineKeyboardButton(text='🛑',
                                                                             callback_data='send_report'),

                                                    ],
                                                    [
                                                        InlineKeyboardButton(text=f'Остановить просмотр анкет',
                                                                             callback_data='stop_finding'),
                                                    ],
                                                ]
                                                )
