from aiogram import types
from aiogram.utils.markdown import hbold


def get_display_name(user: types.User):
    """Возвращает строку с обращением к пользователю, учитывая,
    что у него может отсутствовать username"""
    if user.username:
        return f"@{user.username}"

    return hbold(user.first_name)