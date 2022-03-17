
from aiogram.types import CallbackQuery

from aiogram.dispatcher.filters.builtin import CommandStart
from asyncpg import UniqueViolationError

from keyboards.inline.main_menu import start_keyboard
from loader import dp, db, _
from aiogram import types


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    markup = await start_keyboard()
    try:
        await db.add_user_Users(full_name=message.from_user.full_name,
                                telegram_id=message.from_user.id,
                                username=message.from_user.username)
    except UniqueViolationError:
        pass
    await message.answer(text=_(f"Приветствую вас, {message.from_user.full_name}!!\n\n"
                                f"<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                                f"<b>🤝 Сотрудничество: </b>\n"
                                f"Если у вас есть предложение о сотрудничестве, пишите сюда - "
                                f"@DRomanovizc\n\n"
                                ),
                         reply_markup=markup)


@dp.callback_query_handler(text="start_menu")
async def start_menu(call: CallbackQuery):
    markup = await start_keyboard()
    await call.message.edit_text(text=_(f"Приветствую вас, {call.from_user.full_name}!!\n\n"
                                        f"<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                                        f"<b>🤝 Сотрудничество: </b>\n"
                                        f"Если у вас есть предложение о сотрудничестве, пишите сюда - "
                                        f"@DRomanovizc\n\n"
                                        ),
                                 reply_markup=markup)


@dp.callback_query_handler(text_contains="lang")
async def change_language(call: CallbackQuery):
    await call.message.edit_reply_markup()
    lang = call.data[-2:]

    await call.message.answer(_("Ваш язык был изменен", locale=lang))
