from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

go_back_to_the_menu = InlineKeyboardMarkup(row_width=1,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text="⏪️ Назад", callback_data="submenu")
                                               ]
                                           ])

go_bac_to_second_menu = InlineKeyboardMarkup(row_width=1,
                                             inline_keyboard=[
                                                 [
                                                     InlineKeyboardButton(text="⏪️ Назад", callback_data="secmenu")
                                                 ]
                                             ])
