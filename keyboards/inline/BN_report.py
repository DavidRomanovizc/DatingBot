from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

questionnaires_report_inline_kb = InlineKeyboardMarkup(row_width=5,
                                                       inline_keyboard=[
                                                           [
                                                               InlineKeyboardButton(text='1 🔞',
                                                                                    callback_data='eighteen_plus_content'),

                                                           ],
                                                           [
                                                               InlineKeyboardButton(text='2 💊',
                                                                                    callback_data='drugs')
                                                           ],

                                                           [
                                                               InlineKeyboardButton(text='3 💰',
                                                                                    callback_data='scam'),
                                                           ],

                                                           [
                                                               InlineKeyboardButton(text='4 🦨',
                                                                                    callback_data='another')
                                                           ],
                                                           [
                                                               InlineKeyboardButton(text='5',
                                                                                    callback_data='cancel_3')
                                                           ],

                                                       ])
