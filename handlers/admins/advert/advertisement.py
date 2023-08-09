from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.IsAdminFilter import IsAdmin
from keyboards.admin.inline.mailing import mailing_menu
from keyboards.admin.inline.ref import referral_keyboard
from keyboards.inline.cancel_inline import cancel_keyboard
from loader import dp, _


@dp.message_handler(IsAdmin(), commands="ad", state="*")
@dp.message_handler(IsAdmin(), text="📊 Реклама", state="*")
async def adv_handler(message: Message):
    await message.answer(
        text="<u><b>📊 Реклама</b></u>", reply_markup=await mailing_menu()
    )


@dp.callback_query_handler(IsAdmin(), text="adv:mailing")
async def broadcast_get_text(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(
        text=_(
            "<u><b>📧 Рассылка</b></u>\n"
            "Пришлите текст для рассылки либо фото с текстом для рассылки! Чтобы отредактировать, "
            "используйте встроенный редактор телеграма!\n"
        ),
        reply_markup=await cancel_keyboard()
    )
    await state.set_state("broadcast_get_content")


@dp.callback_query_handler(IsAdmin(), text="adv:ref_urls")
async def ref_handler(call: CallbackQuery):
    await call.message.edit_text(
        text="<u><b>🔗 Реферальные ссылки</b></u>",
        reply_markup=await referral_keyboard()
    )


@dp.callback_query_handler(IsAdmin(), text="adv:required_subs")
async def required_subs_handler(call: CallbackQuery):
    await call.message.edit_text(
        text="<u><b>🧑‍💻 Обязательная подписка</b></u>"
    )
