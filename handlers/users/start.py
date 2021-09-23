from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.inline_start_menu import inline_start
from aiogram.types import CallbackQuery
from loader import dp, db, bot, _
from aiogram import types
import asyncpg


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    try:
        await db.add_user_Users(full_name=message.from_user.full_name,
                                telegram_id=message.from_user.id,
                                username=message.from_user.username,
                                email=None,
                                sex=None,
                                national=None,
                                education=None,
                                city=None,
                                age=None,
                                kids=None,
                                language=None,
                                marital=None,
                                car=None,
                                varname=None,
                                lifestyle=None,
                                is_banned=False,
                                photo_id=None,
                                commentary=None,
                                need_partner_sex=None,
                                likes=None,
                                dislikes=None,
                                apartment=None)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)
        if user.get('is_banned') is not True:
            count_users = await db.count_users()
            await message.reply(text=_(f"Приветствую вас, {message.from_user.full_name}!!\n"
                                       f"Сейчас в нашем боте <b>{count_users}</b> пользователей\n\n"
                                       f"Чтобы увидеть полный список команд - воспользуйтесь командой /help\n\n"),
                                reply_markup=inline_start)
        elif user.get('is_banned') is True:
            await message.answer(f'Вы заблокированы навсегда! За разбл')


# Альтернативно можно использовать фильтр text_contains, он улавливает то, что указано в call.data
@dp.callback_query_handler(text_contains="lang")
async def change_language(call: CallbackQuery):
    await call.message.edit_reply_markup()
    # Достаем последние 2 символа (например ru)
    lang = call.data[-2:]

    # После того, как мы поменяли язык, в этой функции все еще указан старый, поэтому передаем locale=lang
    await call.message.answer(_("Ваш язык был изменен", locale=lang))


@dp.callback_query_handler(text_contains="info")
async def information(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text("<b>Made by: </b>\n"
                                 "\n"
                                 "@DRomanovizc - Team lead\n"
                                 "@mroshalom - Python developer\n"
                                 "@M_O_D_E_R - Python developer \n"
                                 "\n"
                                 "<i>BotScience © 2021</i>",
                                 reply_markup=inline_start)


@dp.callback_query_handler(text_contains="instruction")
async def get_inst(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text(f"<b>Инструкция: </b>\n\n"
                                 f"Тут нужно написать инструкцию\n\n"
                                 f"Если вы нашли баг, то можете сообщить нам, написав сюда\n - @DRomanovizc или @mroshalom",
                                 reply_markup=inline_start)
