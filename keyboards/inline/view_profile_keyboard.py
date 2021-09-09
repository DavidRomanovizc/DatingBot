from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


async def generate_keyboard(liked, disliked):
    view_keyboard = InlineKeyboardMarkup()
    like_btn = InlineKeyboardButton(text=f"👍 - {liked}", callback_data="like")
    dislike_btn = InlineKeyboardButton(text=f"👎 - {disliked}", callback_data="dislike")
    chat_btn = InlineKeyboardButton(text="📝 Написать 📝", callback_data="write_to")
    report_btn = InlineKeyboardButton(text="🛑 Пожаловаться 🛑", callback_data="report")

    view_keyboard.row(like_btn, dislike_btn)
    view_keyboard.add(chat_btn)
    view_keyboard.add(report_btn)

    return view_keyboard
