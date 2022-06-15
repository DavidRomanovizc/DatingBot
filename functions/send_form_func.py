from keyboards.inline.questionnaires_inline import questionnaires_keyboard, back_viewing_ques_keyboard, \
    reciprocity_keyboard
from loader import bot


async def send_questionnaire(chat_id, user_data, user_db, markup=None, add_text=None,
                             monitoring=False):
    user_telegram_id = user_db.get("telegram_id")
    if add_text is None:
        await bot.send_photo(chat_id=chat_id, caption=f"{str(user_data[0])}, "
                                                      f"{str(user_data[1])} лет, "
                                                      f"{str(user_data[3])}\n\n"
                                                      f"<b>О себе</b> - {str(user_data[5])}\n\n"
                                                      f"<b>Инстаграм</b> - <code>{str(user_data[8])}</code>\n"
                                                      f"<b>Статус анкеты - {str(user_data[6])}</b>",
                             photo=user_data[7], reply_markup=await questionnaires_keyboard(target_id=user_telegram_id,
                                                                                            monitoring=monitoring))
    elif markup is None:
        await bot.send_photo(chat_id=chat_id, caption=f"{add_text}\n\n"
                                                      f"{str(user_data[0])}, "
                                                      f"{str(user_data[1])} лет, "
                                                      f"{str(user_data[3])}\n\n"
                                                      f"<b>О себе</b> - {str(user_data[5])}\n\n"
                                                      f"<b>Инстаграм</b> - <code>{str(user_data[8])}</code>\n"
                                                      f"<b>Статус анкеты - {str(user_data[6])}</b>",
                             photo=user_data[7], reply_markup=await back_viewing_ques_keyboard())

    else:
        await bot.send_photo(chat_id=chat_id, caption=f"{add_text}\n\n"
                                                      f"{str(user_data[0])}, "
                                                      f"{str(user_data[1])} лет, "
                                                      f"{str(user_data[3])}\n\n"
                                                      f"<b>О себе</b> - {str(user_data[5])}\n\n"
                                                      f"<b>Инстаграм</b> - <code>{str(user_data[8])}</code>\n"
                                                      f"<b>Статус анкеты - {str(user_data[6])}</b>",
                             photo=user_data[7],
                             reply_markup=await reciprocity_keyboard(user_for_like=user_telegram_id))
