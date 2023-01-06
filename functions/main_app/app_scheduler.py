from aiogram.types import Message

from functions.main_app.get_data_func import get_data
from keyboards.inline.questionnaires_inline import viewing_ques_keyboard
from loader import bot, _


async def send_message_week(message: Message):
    user = await get_data(message.from_user.id)

    if user[10] == "Мужской":
        user_gender = "Парней"
    else:
        user_gender = "Девушек"
    text = _("Несколько {user_gender} из города {city}"
             " хотят познакомиться с тобой прямо сейчас").format(user_gender=user_gender, city=user[12])

    await bot.send_message(chat_id=message.chat.id,
                           text=text,
                           reply_markup=await viewing_ques_keyboard())
