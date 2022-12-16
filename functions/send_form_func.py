from typing import NoReturn

from keyboards.inline.questionnaires_inline import questionnaires_keyboard, back_viewing_ques_keyboard, \
    reciprocity_keyboard
from loader import bot, _


async def send_questionnaire(chat_id, user_data, user_db, markup=None, add_text=None,
                             monitoring=False, report_system=False) -> NoReturn:
    user_telegram_id = user_db.get("telegram_id")
    text_without_inst = _("{user_0}, "
                          "{user_1} лет, "
                          "{user_3} {user_6}\n\n"
                          "{user_5}\n\n").format(user_0=str(user_data[0]),
                                                 user_1=str(user_data[1]),
                                                 user_3=str(user_data[3]),
                                                 user_5=str(user_data[5]),
                                                 user_6=str(user_data[6]))
    text_with_inst = _("{user_0}, "
                       "{user_1} лет, "
                       "{user_3} {user_6}\n\n"
                       "{user_5}\n\n"
                       "<b>Инстаграм</b> - <code>{user_8}</code>\n").format(user_0=str(user_data[0]),
                                                                            user_1=str(user_data[1]),
                                                                            user_3=str(user_data[3]),
                                                                            user_5=str(user_data[5]),
                                                                            user_6=str(user_data[6]),
                                                                            user_8=str(user_data[8]),
                                                                            )
    caption = _("Описание анкеты пользователя.\n\n"
                "<b>Мы не проверяем голосовые сообщения, поэтому советуем"
                " уменьшить громкость звука</b>")

    text_without_description = _("{user_0}, "
                                 "{user_1} лет, "
                                 "{user_3} {user_6}").format(user_0=str(user_data[0]),
                                                             user_1=str(user_data[1]),
                                                             user_3=str(user_data[3]),
                                                             user_6=str(user_data[6]))
    text_voice_with_inst = _("{user_0}, "
                             "{user_1} лет, "
                             "{user_3} {user_6}\n\n"
                             "<b>Инстаграм</b> - <code>{user_8}</code>\n").format(user_0=str(user_data[0]),
                                                                                  user_1=str(user_data[1]),
                                                                                  user_3=str(user_data[3]),
                                                                                  user_6=str(user_data[6]),
                                                                                  user_8=str(user_data[8]),
                                                                                  )
    caption_with_add_text = _("{add_text}\n\n"
                              "{user_0}, "
                              "{user_1} лет, "
                              "{user_3} {user_6}\n\n"
                              "{user_5}\n\n").format(add_text=add_text,
                                                     user_0=str(user_data[0]),
                                                     user_1=str(user_data[1]),
                                                     user_3=str(user_data[3]),
                                                     user_5=str(user_data[5]),
                                                     user_6=str(user_data[6]),
                                                     )
    add_text_with_inst = _("{add_text}\n\n"
                           "{user_0}, "
                           "{user_1} лет, "
                           "{user_3} {user_6}\n\n"
                           "{user_5}\n\n"
                           "<b>Инстаграм</b> - <code>{user_8}</code>\n").format(add_text=add_text,
                                                                                user_0=str(user_data[0]),
                                                                                user_1=str(user_data[1]),
                                                                                user_3=str(user_data[3]),
                                                                                user_5=str(user_data[5]),
                                                                                user_6=str(user_data[6]),
                                                                                user_8=str(user_data[8]),
                                                                                )
    voice_with_add_text = _("{add_text}\n\n"
                            "{user_0}, "
                            "{user_1} лет, "
                            "{user_3} {user_6}\n\n").format(add_text=add_text,
                                                            user_0=str(user_data[0]),
                                                            user_1=str(user_data[1]),
                                                            user_3=str(user_data[3]),
                                                            user_5=str(user_data[5]),
                                                            user_6=str(user_data[6]),
                                                            )
    add_text_without_descr = _("{add_text}\n\n"
                               "{user_0}, "
                               "{user_1} лет, "
                               "{user_3} {user_6}\n\n"
                               "<b>Инстаграм</b> - <code>{user_8}</code>\n").format(add_text=add_text,
                                                                                    user_0=str(user_data[0]),
                                                                                    user_1=str(user_data[1]),
                                                                                    user_3=str(user_data[3]),
                                                                                    user_5=str(user_data[5]),
                                                                                    user_6=str(user_data[6]),
                                                                                    user_8=str(user_data[8]),
                                                                                    )
    if add_text is None and user_data[8] == "Пользователь не прикрепил Instagram" and user_data[11] is None:
        await bot.send_photo(chat_id=chat_id, caption=text_without_inst,
                             photo=user_data[7],
                             reply_markup=await questionnaires_keyboard(target_id=user_telegram_id,
                                                                        monitoring=monitoring,
                                                                        report_system=report_system))
    elif add_text is None and user_data[11] is None:
        await bot.send_photo(chat_id=chat_id, caption=text_with_inst,
                             photo=user_data[7],
                             reply_markup=await questionnaires_keyboard(target_id=user_telegram_id,
                                                                        monitoring=monitoring,
                                                                        report_system=report_system))
    elif add_text is None and user_data[8] == "Пользователь не прикрепил Instagram":

        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user_data[11],
                             protect_content=True, disable_notification=True, duration=60)

        await bot.send_photo(chat_id=chat_id, caption=text_without_description,
                             photo=user_data[7],
                             reply_markup=await questionnaires_keyboard(target_id=user_telegram_id,
                                                                        monitoring=monitoring,
                                                                        report_system=report_system))

    elif add_text is None:
        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user_data[11],
                             protect_content=True, disable_notification=True, duration=60)

        await bot.send_photo(chat_id=chat_id, caption=text_voice_with_inst,
                             photo=user_data[7],
                             reply_markup=await questionnaires_keyboard(target_id=user_telegram_id,
                                                                        monitoring=monitoring,
                                                                        report_system=report_system))

    elif markup is None and user_data[8] == "Пользователь не прикрепил Instagram" and user_data[11] is None:
        await bot.send_photo(chat_id=chat_id, caption=caption_with_add_text,
                             photo=user_data[7], reply_markup=await back_viewing_ques_keyboard())
    elif markup is None and user_data[11] is None:
        await bot.send_photo(chat_id=chat_id, caption=add_text_with_inst,
                             photo=user_data[7], reply_markup=await back_viewing_ques_keyboard())
    elif markup is None and user_data[8] == "Пользователь не прикрепил Instagram":
        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user_data[11],
                             protect_content=True, disable_notification=True, duration=60)
        await bot.send_photo(chat_id=chat_id, caption=voice_with_add_text,
                             photo=user_data[7], reply_markup=await back_viewing_ques_keyboard())

    elif markup is None:
        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user_data[11],
                             protect_content=True, disable_notification=True, duration=60)
        await bot.send_photo(chat_id=chat_id, caption=add_text_without_descr,
                             photo=user_data[7], reply_markup=await back_viewing_ques_keyboard())

    elif user_data[11] is None and user_data[8] == "Пользователь не прикрепил Instagram":
        await bot.send_photo(chat_id=chat_id, caption=caption_with_add_text,
                             photo=user_data[7],
                             reply_markup=await reciprocity_keyboard(user_for_like=user_telegram_id))
    elif user_data[11] is None:
        await bot.send_photo(chat_id=chat_id, caption=add_text_with_inst,
                             photo=user_data[7],
                             reply_markup=await reciprocity_keyboard(user_for_like=user_telegram_id))
    elif user_data[8] == "Пользователь не прикрепил Instagram":
        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user_data[11],
                             protect_content=True, disable_notification=True, duration=60)

        await bot.send_photo(chat_id=chat_id, caption=voice_with_add_text,
                             photo=user_data[7],
                             reply_markup=await reciprocity_keyboard(user_for_like=user_telegram_id))
    else:
        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user_data[11],
                             protect_content=True, disable_notification=True, duration=60)

        await bot.send_photo(chat_id=chat_id, caption=add_text_without_descr,
                             photo=user_data[7],
                             reply_markup=await reciprocity_keyboard(user_for_like=user_telegram_id))
