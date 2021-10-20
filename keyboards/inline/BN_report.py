from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

report_inline_kb = InlineKeyboardMarkup(row_width=2,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text='🔞',
                                                                     callback_data='content'),

                                            ],
                                            [
                                                InlineKeyboardButton(text='💊',
                                                                     callback_data='drugs')
                                            ],

                                            [
                                                InlineKeyboardButton(text='💰',
                                                                     callback_data='scam'),
                                            ],

                                            [
                                                InlineKeyboardButton(text='🦨',
                                                                     callback_data='another')
                                            ],
                                            [
                                                InlineKeyboardButton(text='❌',
                                                                     callback_data='cancel_report')
                                            ],

                                        ])
