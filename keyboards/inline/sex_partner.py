from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btn_partner = InlineKeyboardMarkup(row_width=2,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text='Мужчин',
                                                                callback_data='gen_male'),
                                           InlineKeyboardButton(text='Женщин',
                                                                callback_data='female'),
                                       ]
                                   ]
                                   )
