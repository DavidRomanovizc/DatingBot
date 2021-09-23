from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_start = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=
                                        [
                                            [
                                                InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
                                                InlineKeyboardButton(text="English", callback_data="lang_en")
                                            ],

                                            [
                                                InlineKeyboardButton(text="Информация", callback_data="info")
                                            ],
                                            [
                                                InlineKeyboardButton(text="Зарегистрироваться",
                                                                     callback_data="registration"),
                                                InlineKeyboardButton(text="Меню бота",
                                                                     callback_data="menu")
                                            ],
                                            [
                                                InlineKeyboardButton(text="Поддержка проекта", callback_data="Donation")
                                            ]
                                        ])
