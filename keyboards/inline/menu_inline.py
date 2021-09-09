from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_inline_kb = InlineKeyboardMarkup(row_width=3,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Моя анекта',
                                                                   callback_data='my_profile'),

                                              InlineKeyboardButton(text='Изменить анкету',
                                                                   callback_data='change_profile')
                                          ],

                                          [
                                              InlineKeyboardButton(text='Смотреть анкеты',
                                                                   callback_data='find_ancets'),
                                              InlineKeyboardButton(text='Мои предпочтения',
                                                                   callback_data='preferences')
                                          ],

                                          [
                                              InlineKeyboardButton(text='Я больше не хочу никого искать',
                                                                   callback_data='cancel')
                                          ],

                                      ]
                                      )

btn_pref = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Мужчин',
                                                             callback_data='gen_male'),
                                        InlineKeyboardButton(text='Женщин',
                                                             callback_data='g_fe'),
                                    ],
                                ]
                                )
