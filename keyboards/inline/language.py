from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

languages_markup = InlineKeyboardMarkup(row_width=2,
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
                                                                     callback_data="menusion")
                                            ],
                                            [
                                                InlineKeyboardButton(text="Поддержка проекта", callback_data="Donation")
                                            ]
                                        ])
