from aiogram import types
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.utils.exceptions import MessageCantBeDeleted

from keyboards.inline.guide_inline import first_str_keyboard, second_str_keyboard, third_str_keyboard, \
    fourth_str_keyboard
from loader import dp, bot, _


@dp.callback_query_handler(text_contains="info")
async def get_information(call: CallbackQuery) -> None:
    markup = await first_str_keyboard()
    photo = r"brandbook/first_page.png"
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_photo(chat_id=call.from_user.id, photo=types.InputFile(photo),
                             reply_markup=markup, caption=_("Руководство по боту: \n<b>Страница №1</b>"))
    except MessageCantBeDeleted:
        pass


@dp.callback_query_handler(text="forward_f")
async def get_forward(call: CallbackQuery) -> None:
    markup = await second_str_keyboard()
    photo = r"brandbook/second_page.png"
    photo = InputMediaPhoto(
        media=types.InputFile(photo),
        caption=_("Руководство по боту: \n<b>Страница №2</b>"))
    await call.message.edit_media(photo, reply_markup=markup)


@dp.callback_query_handler(text="backward_s")
async def get_backward_f(call: CallbackQuery) -> None:
    markup = await first_str_keyboard()
    photo = r"brandbook/first_page.png"
    photo = InputMediaPhoto(
        media=types.InputFile(photo),
        caption=_("Руководство по боту: \n<b>Страница №1</b>")
    )
    await call.message.edit_media(photo, reply_markup=markup)


@dp.callback_query_handler(text="forward_s")
async def get_forward_s(call: CallbackQuery) -> None:
    markup = await third_str_keyboard()
    photo = r"brandbook/third_page.png"
    photo = InputMediaPhoto(
        media=types.InputFile(photo),
        caption=_("Руководство по боту: \n<b>Страница №3</b>"))
    await call.message.edit_media(photo, reply_markup=markup)


@dp.callback_query_handler(text="backward_th")
async def get_backward_f(call: CallbackQuery) -> None:
    markup = await second_str_keyboard()
    photo = r"brandbook/second_page.png"
    photo = InputMediaPhoto(
        media=types.InputFile(photo),
        caption=_("Руководство по боту: \n<b>Страница №2</b>")
    )
    await call.message.edit_media(photo, reply_markup=markup)


@dp.callback_query_handler(text="forward_th")
async def get_backward_f(call: CallbackQuery) -> None:
    markup = await fourth_str_keyboard()
    photo = r"brandbook/fourth_page.png"
    photo = InputMediaPhoto(
        media=types.InputFile(photo),
        caption=_("Руководство по боту: \n<b>Страница №4</b>")
    )
    await call.message.edit_media(photo, reply_markup=markup)


@dp.callback_query_handler(text="backward_four")
async def get_backward_f(call: CallbackQuery) -> None:
    markup = await third_str_keyboard()
    photo = r"brandbook/third_page.png"
    photo = InputMediaPhoto(
        media=types.InputFile(photo),
        caption=_("Руководство по боту: \n<b>Страница №3</b>")
    )
    await call.message.edit_media(photo, reply_markup=markup)
