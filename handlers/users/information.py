from keyboards.inline.guide_inline import first_str_keyboard, second_str_keyboard, third_str_keyboard, fourth_str_keyboard
from aiogram.types import CallbackQuery, InputMediaPhoto
from loader import dp, bot


@dp.callback_query_handler(text_contains="info")
async def get_information(call: CallbackQuery):
    markup = await first_str_keyboard()
    photo = r"https://sun9-39.userapi.com/impg/UELKd0082Jj7ysgbotGiJ-7_3KUKDZU3kAOmdg/u2jMOCYI7uA.jpg?size=2166x2160&quality=96&sign=2d19e64e60ca10bc883c18251530c435&type=album"
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_photo(chat_id=call.from_user.id,
                         photo=photo,
                         caption="Руководство по боту: \n<b>Страница №1</b>", reply_markup=markup)


@dp.callback_query_handler(text="forward_f")
async def get_forward(call: CallbackQuery):
    markup = await second_str_keyboard()
    photo = InputMediaPhoto(
        "https://sun9-45.userapi.com/impg/449qcPuHzpdJGJ4gkj7CxnVOshAT5Yvrd6B3Pw/F9ywn4_l-W8.jpg?size=1086x1083&quality=96&sign=2c1fdb7c9f2a21e1e96843d1973c4266&type=album",
        caption="Руководство по боту: \n<b>Страница №2</b>")
    await call.message.edit_media(photo, reply_markup=markup)


@dp.callback_query_handler(text="backward_s")
async def get_backward_f(call: CallbackQuery):
    markup = await first_str_keyboard()
    photo = InputMediaPhoto(
        "https://sun9-39.userapi.com/impg/UELKd0082Jj7ysgbotGiJ-7_3KUKDZU3kAOmdg/u2jMOCYI7uA.jpg?size=2166x2160&quality=96&sign=2d19e64e60ca10bc883c18251530c435&type=album",
        caption="Руководство по боту: \n<b>Страница №1</b>"
    )
    await call.message.edit_media(photo, reply_markup=markup)


@dp.callback_query_handler(text="forward_s")
async def get_forward_s(call: CallbackQuery):
    markup = await third_str_keyboard()
    photo = InputMediaPhoto(
        "https://sun9-37.userapi.com/impg/jVNgiTMNgqY6obppE8sgPyWV4gEcVN7963sYdw/PJcospk0cLM.jpg?size=1086x1083&quality=96&sign=ce373d4b07baad45680ddad5c697781a&type=album",
        caption="Руководство по боту: \n<b>Страница №3</b>")
    await call.message.edit_media(photo, reply_markup=markup)


@dp.callback_query_handler(text="backward_th")
async def get_backward_f(call: CallbackQuery):
    markup = await second_str_keyboard()
    photo = InputMediaPhoto(
        "https://sun9-37.userapi.com/impg/jVNgiTMNgqY6obppE8sgPyWV4gEcVN7963sYdw/PJcospk0cLM.jpg?size=1086x1083&quality=96&sign=ce373d4b07baad45680ddad5c697781a&type=album",
        caption="Руководство по боту: \n<b>Страница №2</b>"
    )
    await call.message.edit_media(photo, reply_markup=markup)


@dp.callback_query_handler(text="forward_th")
async def get_backward_f(call: CallbackQuery):
    markup = await fourth_str_keyboard()
    photo = InputMediaPhoto(
        "https://sun9-58.userapi.com/impg/9c8V5OPSMiEHmHXSHMEYcjkxLGYNCtcEhXbddw/58PJ7C2ZoM0.jpg?size=2166x2160&quality=96&sign=4e8859f03f06ed6cc6f7c42e84453362&type=album",
        caption="Руководство по боту: \n<b>Страница №4</b>"
    )
    await call.message.edit_media(photo, reply_markup=markup)


@dp.callback_query_handler(text="backward_four")
async def get_backward_f(call: CallbackQuery):
    markup = await third_str_keyboard()
    photo = InputMediaPhoto(
        "https://sun9-37.userapi.com/impg/jVNgiTMNgqY6obppE8sgPyWV4gEcVN7963sYdw/PJcospk0cLM.jpg?size=1086x1083&quality=96&sign=ce373d4b07baad45680ddad5c697781a&type=album",
        caption="Руководство по боту: \n<b>Страница №3</b>"
    )
    await call.message.edit_media(photo, reply_markup=markup)
