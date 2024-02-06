from typing import (
    Optional,
)

from aiogram.types import (
    InlineKeyboardMarkup,
)
from aiogram.utils.exceptions import (
    BadRequest,
)

from keyboards.admin.inline.customers import (
    user_blocking_keyboard,
)
from keyboards.inline.questionnaires_inline import (
    questionnaires_keyboard,
    reciprocity_keyboard,
)
from loader import (
    _,
    bot,
    logger,
)
from utils.db_api import (
    db_commands,
)


async def send_questionnaire(
        chat_id: int,
        owner_id: Optional[int] = None,
        markup: Optional[InlineKeyboardMarkup] = None,
        add_text: Optional[str] = None,
        monitoring: bool = False,
        report_system: bool = False,
) -> None:
    user = await db_commands.select_user(owner_id)
    text_template = _("{}, {} лет, {} {verification}\n\n")
    user_verification = "✅" if user.verification else ""

    text_without_inst = _(text_template + "{commentary}").format(
        user.varname,
        user.age,
        user.city,
        commentary=user.commentary,
        verification=user_verification,
    )

    text_with_inst_template = text_template + _(
        "<b>Инстаграм</b> - <code>{instagram}</code>\n"
    )
    text_with_inst = _(text_with_inst_template).format(
        user.varname,
        user.age,
        user.city,
        user.commentary,
        verification=user_verification,
        instagram=user.instagram,
    )

    caption_with_add_text = _("{}\n\n" + text_template + "{}").format(
        add_text,
        user.varname,
        user.age,
        user.city,
        user.commentary,
        verification=user_verification,
    )

    add_text_with_inst = _(
        "{}\n\n" + text_template + "<b>Инстаграм</b> - <code>{instagram}</code>\n"
    ).format(
        add_text,
        user.varname,
        user.age,
        user.city,
        user.commentary,
        verification=user_verification,
        instagram=user.instagram,
    )
    try:
        if add_text is None and user.instagram is None:
            await bot.send_photo(
                chat_id=chat_id,
                caption=text_without_inst,
                photo=user.photo_id,
                reply_markup=await questionnaires_keyboard(
                    target_id=owner_id, monitoring=monitoring
                ),
            )
        elif add_text is None:
            await bot.send_photo(
                chat_id=chat_id,
                caption=text_with_inst,
                photo=user.photo_id,
                reply_markup=await questionnaires_keyboard(
                    target_id=owner_id, monitoring=monitoring
                ),
            )
        elif markup is None and user.instagram is None:
            await bot.send_photo(
                chat_id=chat_id,
                caption=caption_with_add_text,
                photo=user.photo_id,
            )
        elif markup is None:
            await bot.send_photo(
                chat_id=chat_id, caption=add_text_with_inst, photo=user.photo_id
            )
        elif user.instagram is None and not report_system:
            await bot.send_photo(
                chat_id=chat_id,
                caption=caption_with_add_text,
                photo=user.photo_id,
                reply_markup=await reciprocity_keyboard(user_for_like=owner_id),
            )
        elif report_system:
            await bot.send_photo(
                chat_id=chat_id,
                caption=add_text,
                photo=user.photo_id,
                reply_markup=await user_blocking_keyboard(
                    user_id=owner_id, is_banned=user.is_banned
                ),
            )
        else:
            await bot.send_photo(
                chat_id=chat_id,
                caption=add_text_with_inst,
                photo=user.photo_id,
                reply_markup=await reciprocity_keyboard(user_for_like=owner_id),
            )
    except BadRequest as err:
        logger.info(f"{err}. Error in the send_questionnaire function")
