from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

reg_profile = InlineKeyboardMarkup(row_width=3,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text="Пройти опрос", callback_data="survey")
                                       ],
                                   ])
