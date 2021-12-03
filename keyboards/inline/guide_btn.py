from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btn_guide = InlineKeyboardMarkup(row_width=3,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text='⬅️ Назад',
                                                              callback_data='backward'),
                                         InlineKeyboardButton(text='➡️ Вперед',
                                                              callback_data='forward')

                                     ],

                                     [
                                         InlineKeyboardButton(text='❌ Закрыть',
                                                              callback_data='close_everything')
                                     ],
                                 ]
                                 )
