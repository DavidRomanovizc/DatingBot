from keyboards.inline.main_menu import inline_start
from aiogram.types import CallbackQuery

from aiogram.dispatcher.filters.builtin import CommandStart
from asyncpg import UniqueViolationError

from loader import dp, db, _
from aiogram import types


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    try:
        await db.add_user_Users(full_name=message.from_user.full_name,
                                telegram_id=message.from_user.id,
                                username=message.from_user.username)
    except UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)
        if user.get('is_banned') is not True:
            count_users = await db.count_users()
            await message.reply(text=_(f"Приветствую вас, {message.from_user.full_name}!!\n"
                                       f"Сейчас в нашем боте <b>{count_users}</b> пользователей\n\n"
                                       f"Чтобы увидеть полный список команд - воспользуйтесь командой /help\n\n"),
                                reply_markup=inline_start)
        elif user.get('is_banned') is True:
            await message.answer(f'Вы заблокированы навсегда! За разблокировкой пишите админу')


@dp.callback_query_handler(text_contains="lang")
async def change_language(call: CallbackQuery):
    await call.message.edit_reply_markup()
    lang = call.data[-2:]

    await call.message.answer(_("Ваш язык был изменен", locale=lang))
