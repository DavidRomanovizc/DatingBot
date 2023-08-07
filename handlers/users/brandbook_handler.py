from datetime import datetime

from aiogram.types import CallbackQuery

from functions.main_app.auxiliary_tools import send_photo_with_caption, handle_guide_callback
from keyboards.inline.back_inline import only_back_keyboard
from keyboards.inline.guide_inline import guide_callback
from keyboards.inline.settings_menu import information_keyboard
from loader import dp, _
from utils.db_api import db_commands


@dp.callback_query_handler(text="information")
async def get_information(call: CallbackQuery):
    start_date = datetime(2021, 8, 10, 14, 0)
    now_date = datetime.now()
    delta = now_date - start_date
    count_users = await db_commands.count_users()
    txt = _("Вы попали в раздел <b>Информации</b> бота, здесь вы можете посмотреть: статистику,"
            "изменить язык, а также посмотреть наш брендбук.\n\n"
            "🌐 Дней работаем: <b>{}</b>\n"
            "👤 Всего пользователей: <b>{}</b>\n").format(delta.days, count_users)
    await call.message.edit_text(
        text=txt,
        reply_markup=await information_keyboard()
    )


@dp.callback_query_handler(text="guide")
async def get_guide(call: CallbackQuery) -> None:
    await send_photo_with_caption(
        call=call,
        photo=r"brandbook/1_page.png",
        caption=_("Руководство по боту: \n<b>Страница №1</b>"),
        step=1,
        total_steps=4
    )


@dp.callback_query_handler(guide_callback.filter(action=["forward", "backward"]))
async def get_forward(call: CallbackQuery, callback_data: dict) -> None:
    await handle_guide_callback(call, callback_data)


@dp.callback_query_handler(text="contacts")
async def contacts_menu(call: CallbackQuery):
    await call.message.edit_text(
        text=(
            "📧 Добро пожаловать в наш раздел контактной информации платформы:\n\n"
            "Наш сайт: В разработке"
        ),
        reply_markup=await only_back_keyboard(menu="information")
    )
