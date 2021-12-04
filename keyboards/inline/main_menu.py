from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_start = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=
                                    [
                                        [
                                            InlineKeyboardButton(text="➕ Регистрация",
                                                                 callback_data="registration"),
                                            InlineKeyboardButton(text="📄 Меню бота",
                                                                 callback_data="second_m")
                                        ],
                                        [
                                            InlineKeyboardButton(text="🌐 Информация", callback_data="info")
                                        ],

                                        [
                                            InlineKeyboardButton(text="💚 Спонсорство",
                                                                 url="https://www.donationalerts.com/r/david_romanov"),
                                            InlineKeyboardButton(text="📈 Статистика", callback_data="statistics")
                                        ]
                                    ]
                                    )
