from typing import NoReturn

from keyboards.inline.questionnaires_inline import questionnaires_keyboard, back_viewing_ques_keyboard, \
    reciprocity_keyboard
from loader import bot, _
from utils.db_api import db_commands


async def send_questionnaire(chat_id, owner_id, markup=None, add_text=None,
                             monitoring=False, report_system=False) -> NoReturn:
    user = await db_commands.select_user(owner_id)
    text_template = "{}, {} лет, {} {verification}\n\n"
    user_verification = "✅" if user["verification"] else "❌"

    text_without_inst = _(text_template + "{commentary}").format(user.get("varname"),
                                                                 user.get("age"),
                                                                 user.get("city"),
                                                                 commentary=user.get("commentary"),
                                                                 verification=user_verification)

    text_with_inst_template = text_template + "<b>Инстаграм</b> - <code>{instagram}</code>\n"
    text_with_inst = _(text_with_inst_template).format(user.get("varname"),
                                                       user.get("age"),
                                                       user.get("city"),
                                                       user.get("commentary"),
                                                       verification=user_verification,
                                                       instagram=user.get("instagram"))

    caption = _("Описание анкеты пользователя.\n\n"
                "<b>Мы не проверяем голосовые сообщения, поэтому советуем"
                " уменьшить громкость звука</b>")

    text_without_description = text_template.format(user.get("varname"),
                                                    user.get("age"),
                                                    user.get("city"),
                                                    verification=user_verification)
    text_voice_with_inst = (text_template + "<b>Инстаграм</b> - <code>{instagram}</code>\n").format(
        user.get("varname"),
        user.get("age"),
        user.get("city"),
        verification=user_verification,
        instagram=user.get("instagram"),
    )

    caption_with_add_text = _("{}\n\n" + text_template + "{}").format(add_text,
                                                                      user.get("varname"),
                                                                      user.get("age"),
                                                                      user.get("city"),
                                                                      user.get("commentary"),
                                                                      verification=user_verification)

    add_text_with_inst = _("{}\n\n" + text_template +
                           "<b>Инстаграм</b> - <code>{instagram}</code>\n").format(add_text,
                                                                                   user.get("varname"),
                                                                                   user.get("age"),
                                                                                   user.get("city"),
                                                                                   user.get("commentary"),
                                                                                   verification=user_verification,
                                                                                   instagram=user.get("instagram"))

    voice_with_add_text = _(text_template).format(add_text,
                                                  user.get("varname"),
                                                  user.get("age"),
                                                  user.get("city"),
                                                  verification=user_verification)
    add_text_without_descr = _(text_template +
                               "<b>Инстаграм</b> - <code>{instagram}</code>\n").format(add_text,
                                                                                       user.get("varname"),
                                                                                       user.get("age"),
                                                                                       user.get("city"),
                                                                                       verification=user_verification,
                                                                                       instagram=user.get("instagram"))
    if add_text is None and user.get("instagram") is None and user.get("voice_id") is None:
        await bot.send_photo(chat_id=chat_id, caption=text_without_inst,
                             photo=user.get("photo_id"),
                             reply_markup=await questionnaires_keyboard(target_id=owner_id,
                                                                        monitoring=monitoring,
                                                                        report_system=report_system))
    elif add_text is None and user.get("voice_id") is None:
        await bot.send_photo(chat_id=chat_id, caption=text_with_inst,
                             photo=user.get("photo_id"),
                             reply_markup=await questionnaires_keyboard(target_id=owner_id,
                                                                        monitoring=monitoring,
                                                                        report_system=report_system))
    elif add_text is None and user.get("instagram") is None:

        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user.get("voice_id"),
                             protect_content=True, disable_notification=True, duration=60)

        await bot.send_photo(chat_id=chat_id, caption=text_without_description,
                             photo=user.get("photo_id"),
                             reply_markup=await questionnaires_keyboard(target_id=owner_id,
                                                                        monitoring=monitoring,
                                                                        report_system=report_system))
    elif add_text is None:
        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user.get("voice_id"),
                             protect_content=True, disable_notification=True, duration=60)

        await bot.send_photo(chat_id=chat_id, caption=text_voice_with_inst,
                             photo=user.get("photo_id"),
                             reply_markup=await questionnaires_keyboard(target_id=owner_id,
                                                                        monitoring=monitoring,
                                                                        report_system=report_system))

    elif markup is None and user.get("instagram") is None and user.get("voice_id") is None:
        await bot.send_photo(chat_id=chat_id, caption=caption_with_add_text,
                             photo=user.get("photo_id"), reply_markup=await back_viewing_ques_keyboard())
    elif markup is None and user.get("voice_id") is None:
        await bot.send_photo(chat_id=chat_id, caption=add_text_with_inst,
                             photo=user.get("photo_id"), reply_markup=await back_viewing_ques_keyboard())
    elif markup is None and user.get("instagram") is None:
        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user.get("voice_id"),
                             protect_content=True, disable_notification=True, duration=60)
        await bot.send_photo(chat_id=chat_id, caption=voice_with_add_text,
                             photo=user.get("photo_id"), reply_markup=await back_viewing_ques_keyboard())

    elif markup is None:
        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user.get("voice_id"),
                             protect_content=True, disable_notification=True, duration=60)
        await bot.send_photo(chat_id=chat_id, caption=add_text_without_descr,
                             photo=user.get("photo_id"), reply_markup=await back_viewing_ques_keyboard())

    elif user.get("voice_id") is None and user.get("instagram") is None:
        await bot.send_photo(chat_id=chat_id, caption=caption_with_add_text,
                             photo=user.get("photo_id"),
                             reply_markup=await reciprocity_keyboard(user_for_like=owner_id))
    elif user.get("voice_id") is None:
        await bot.send_photo(chat_id=chat_id, caption=add_text_with_inst,
                             photo=user.get("photo_id"),
                             reply_markup=await reciprocity_keyboard(user_for_like=owner_id))
    elif user.get("instagram") is None:
        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user.get("voice_id"),
                             protect_content=True, disable_notification=True, duration=60)

        await bot.send_photo(chat_id=chat_id, caption=voice_with_add_text,
                             photo=user.get("photo_id"),
                             reply_markup=await reciprocity_keyboard(user_for_like=owner_id))
    else:
        await bot.send_voice(chat_id=chat_id, caption=caption, voice=user.get("voice_id"),
                             protect_content=True, disable_notification=True, duration=60)

        await bot.send_photo(chat_id=chat_id, caption=add_text_without_descr,
                             photo=user.get("photo_id"),
                             reply_markup=await reciprocity_keyboard(user_for_like=owner_id))
