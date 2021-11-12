from aiogram.dispatcher.filters.builtin import CommandStart
from asyncpg import UniqueViolationError

from keyboards.inline.inline_start_menu import inline_start
from aiogram.types import CallbackQuery
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


@dp.callback_query_handler(text_contains="info")
async def information(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text("<b>Made by: </b>\n"
                                 "\n"
                                 "@DRomanovizc - Python Developer\n"
                                 "@mroshalom - Python Developer\n"
                                 "\n"
                                 "ПОЛЬЗУЯСЬ БОТОМ ВЫ АВТОМАТИЧЕСКИ СОГЛАШАЕТЕСЬ НА ОБРАБОТКУ ПЕРСОНАЛЬНЫХ ДАННЫХ\n"
                                 "<i>Dslango© 2021</i>",
                                 reply_markup=inline_start)


@dp.callback_query_handler(text_contains="instruction")
async def get_inst(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text(f"<b>Инструкция: </b>\n\n"
                                 f"<b>1. Навигация по анкетам\n\n</b>"
                                 f"👍 - <i>вам понравилась анкета другого пользователя</i>\n"
                                 f"👎 - <i>вам не понравилась анкета</i>\n"
                                 f"💌 - <i>отправить через бота сообщение</i>\n"
                                 f"🛑 - <i>пожаловаться на анкету/пользователя</i>\n\n"
                                 f"Если вы нашли баг, то можете сообщить нам, написав сюда\n - @DRomanovizc или "
                                 f"@mroshalom",
                                 reply_markup=inline_start)
