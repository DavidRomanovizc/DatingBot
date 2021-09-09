from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

change_profile_kb = ReplyKeyboardMarkup(row_width=2,
                                        resize_keyboard=True,
                                        keyboard=[
                                            [
                                                KeyboardButton(text='Имя'),
                                                KeyboardButton(text='Пол'),
                                                KeyboardButton(text='Возраст'),
                                                KeyboardButton(text='Национальность'),
                                                KeyboardButton(text='Город')
                                            ],
                                            [
                                                KeyboardButton(text='Образование'),
                                                KeyboardButton(text='Машина'),
                                                KeyboardButton(text='Жилье'),
                                                KeyboardButton(text='Занятие'),
                                                KeyboardButton(text='Дети'),

                                            ],
                                            [
                                                KeyboardButton(text='Фото')
                                            ],
                                            [
                                                KeyboardButton(text='О себе')
                                            ],
                                        ])