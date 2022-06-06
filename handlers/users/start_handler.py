from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from loguru import logger

from handlers.users.back_handler import hearts
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp, _
from utils.db_api import db_commands


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    markup = await start_keyboard()
    try:
        if message.from_user.username is not None:
            await db_commands.add_user(name=message.from_user.full_name,
                                       telegram_id=message.from_user.id,
                                       username=message.from_user.username)
            await db_commands.add_meetings_user(telegram_id=message.from_user.id,
                                                username=message.from_user.username)
        else:
            await db_commands.add_user(name=message.from_user.full_name,
                                       telegram_id=message.from_user.id,
                                       username="None")
            await db_commands.add_meetings_user(telegram_id=message.from_user.id,
                                                username="None")

    except:
        pass
    await message.answer(text=_(f"Приветствую вас, {message.from_user.full_name}!!\n\n"
                                f"<b>{hearts[2]} DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                                f"<b>🤝 Сотрудничество: </b>\n"
                                f"Если у вас есть предложение о сотрудничестве, пишите сюда - "
                                f"@Support\n\n"
                                ),
                         reply_markup=markup)


@dp.callback_query_handler(text="start_menu")
async def start_menu(call: CallbackQuery):
    markup = await start_keyboard()
    await call.message.edit_text(text=_(f"Приветствую вас, {call.from_user.full_name}!!\n\n"
                                        f"<b>❤ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                                        f"<b>🤝 Сотрудничество: </b>\n"
                                        f"Если у вас есть предложение о сотрудничестве, пишите сюда - "
                                        f"@Support\n\n"
                                        ),
                                 reply_markup=markup)


@dp.callback_query_handler(text_contains="lang")
async def change_language(call: CallbackQuery):
    await call.message.edit_reply_markup()
    lang = call.data[-2:]
    await call.message.answer(_("Ваш язык был изменен", locale=lang))
