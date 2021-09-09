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
