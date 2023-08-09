from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from filters.IsAdminFilter import IsAdmin
from keyboards.admin.inline.payments import payments_keyboard
from loader import dp


@dp.message_handler(IsAdmin(), commands="payments", state="*")
@dp.message_handler(IsAdmin(), text="💳 Платежки", state="*")
async def command_start(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<u>💳 Платежки</u>", reply_markup=await payments_keyboard())