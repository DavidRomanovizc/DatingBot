from aiogram import types
from aiogram.utils.markdown import hbold


def get_display_name(user: types.User) -> str:
    if user.username:
        return f"@{user.username}"

    return hbold(user.first_name)
