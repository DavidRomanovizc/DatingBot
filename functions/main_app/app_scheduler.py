from aiogram.types import Message

from keyboards.inline.questionnaires_inline import viewing_ques_keyboard
from loader import bot, _
from utils.db_api import db_commands


async def send_message_week(message: Message):
    user = await db_commands.select_user(telegram_id=message.from_user.id)

    if user.get("need_partner_sex") == "Мужской":
        user_gender = "Парней"
    else:
        user_gender = "Девушек"
    text = _("Несколько {} из города {}"
             " хотят познакомиться с тобой прямо сейчас").format(user_gender, user.get("need_city"))

    await bot.send_message(chat_id=message.chat.id,
                           text=text,
                           reply_markup=await viewing_ques_keyboard())
