from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

first_str = InlineKeyboardMarkup(row_width=3,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text='➡️ Вперед',
                                                              callback_data='forward_f')
                                     ],

                                     [
                                         InlineKeyboardButton(text='❌ Закрыть',
                                                              callback_data='close_everything')
                                     ],
                                 ]
                                 )

second_str = InlineKeyboardMarkup(row_width=3,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='⬅️ Назад',
                                                               callback_data='backward_s'),
                                          InlineKeyboardButton(text='➡️ Вперед',
                                                               callback_data='forward_s')

                                      ],

                                      [
                                          InlineKeyboardButton(text='❌ Закрыть',
                                                               callback_data='close_everything')
                                      ],
                                  ]
                                  )

third_str = InlineKeyboardMarkup(row_width=3,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text='⬅️ Назад',
                                                              callback_data='backward_th'),
                                         InlineKeyboardButton(text='➡️ Вперед',
                                                              callback_data='forward_th')
                                     ],

                                     [
                                         InlineKeyboardButton(text='❌ Закрыть',
                                                              callback_data='close_everything')
                                     ],
                                 ]
                                 )

fourth_str = InlineKeyboardMarkup(row_width=3,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='⬅️ Назад',
                                                               callback_data='backward_four'),
                                      ],

                                      [
                                          InlineKeyboardButton(text='❌ Закрыть',
                                                               callback_data='close_everything')
                                      ],
                                  ]
                                  )
