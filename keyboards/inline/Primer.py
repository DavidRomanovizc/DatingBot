##############################################
#                FROZEN                     ##
#             INDEFINITELY                  ##
#############################################

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def prime_buy(item_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Купить", callback_data=f"buy:{item_id}")
            ]
        ]
    )
    return keyboard


paid_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Оплатил",
                callback_data="paid")
        ],
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data="cancel_2")
        ],
    ]
)

choice_payment = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text="Qiwi", callback_data="qiwi_pay")
                                          ],
                                          [
                                              InlineKeyboardButton(text="ЮKassa", callback_data="ykassa_pay")
                                          ],
                                          [
                                              InlineKeyboardButton(text="Назад", callback_data="cancel")
                                          ]
                                      ])