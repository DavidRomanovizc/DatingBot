from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode
from loguru import logger

from loader import dp, _


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    text = _("Эхо без состояния.",
             "Сообщение:\n {hcode(message.text)}").__format__(hcode(message.text))

    await message.answer(text)


@dp.message_handler(state="*")
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Эхо в состоянии {hcode(state_name)}',
        'Содержание сообщения:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text))


@dp.callback_query_handler()
async def cq_echo(call: CallbackQuery):
    logger.debug(call.data)
