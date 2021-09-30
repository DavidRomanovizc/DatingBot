from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_start = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=
                                    [
                                        [
                                            InlineKeyboardButton(text="Регистрация",
                                                                 callback_data="registration"),
                                            InlineKeyboardButton(text="Меню бота",
                                                                 callback_data="menu")
                                        ],
                                        [
                                            InlineKeyboardButton(text="Информация", callback_data="info")
                                        ],

                                        [
                                            InlineKeyboardButton(text="Поддержка проекта", callback_data="Donation"),
                                            InlineKeyboardButton(text="Инструкция", callback_data="instruction")
                                        ]
                                    ])
