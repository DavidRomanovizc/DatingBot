import asyncio
import random
import secrets
from abc import ABC, abstractmethod

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import load_config
from functions.dating.create_forms_funcs import (
    create_questionnaire,
    rand_user_list,
    create_questionnaire_reciprocity
)
from functions.dating.get_next_user_func import get_next_user
from functions.main_app.auxiliary_tools import get_report_reason
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.questionnaires_inline import (
    user_link_keyboard, report_menu_keyboard
)
from loader import bot, _
from utils.db_api import db_commands


class ActionStrategy(ABC):
    @abstractmethod
    async def execute(
            self,
            call: CallbackQuery,
            state: FSMContext,
            callback_data: dict[str, str]
    ):
        pass


class StartFindingSuccess(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, **kwargs):
        await call.message.delete()
        telegram_id = call.from_user.id
        user_list = await get_next_user(telegram_id)
        random_user = random.choice(user_list)
        await create_questionnaire(form_owner=random_user, chat_id=telegram_id)
        await state.set_state("finding")


class StartFindingFailure(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, **kwargs):
        await call.answer(_("На данный момент у нас нет подходящих анкет для вас"))


class StartFindingReachLimit(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, **kwargs):
        await call.answer(
            text=_("У вас достигнут лимит на просмотры анкет"),
            show_alert=True
        )


class LikeAction(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, callback_data: dict[str, str]):
        user = await db_commands.select_user_object(telegram_id=call.from_user.id)
        text = _("Кому-то понравилась твоя анкета")
        target_id = int(callback_data["target_id"])

        await create_questionnaire(
            form_owner=call.from_user.id,
            chat_id=target_id,
            add_text=text
        )

        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=None
        )

        await db_commands.update_user_data(
            telegram_id=call.from_user.id,
            limit_of_views=user.limit_of_views - 1
        )
        await create_questionnaire(
            form_owner=(await rand_user_list(call)),
            chat_id=call.from_user.id
        )

        await state.reset_data()


class DislikeAction(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, callback_data: dict[str, str]):
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        await create_questionnaire(
            form_owner=(await rand_user_list(call)),
            chat_id=call.from_user.id
        )
        await state.reset_data()


class StoppedAction(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, callback_data: dict[str, str]):
        text = _("Рад был помочь, {fullname}!\nНадеюсь, ты нашел кого-то благодаря мне").format(
            fullname=call.from_user.full_name)
        await call.answer(text, show_alert=True)
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=await start_keyboard(call)
        )
        await state.reset_state()


class LikeReciprocity(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, callback_data: dict[str, str]):
        user_for_like = int(callback_data["user_for_like"])
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        await call.message.answer(
            text=_("Отлично! Надеюсь вы хорошо проведете время ;) Начинай общаться 👉"),
            reply_markup=await user_link_keyboard(telegram_id=user_for_like)
        )
        await create_questionnaire_reciprocity(
            liker=call.from_user.id,
            chat_id=user_for_like,
            add_text=""
        )
        await bot.send_message(
            chat_id=user_for_like,
            text="Есть взаимная симпатия! Начиная общаться 👉",
            reply_markup=await user_link_keyboard(telegram_id=call.from_user.id)
        )
        await state.reset_state()


class DislikeReciprocity(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, callback_data: dict[str, str]):
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=await start_keyboard(call)
        )
        await state.reset_state()


class GoBackToViewing(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, callback_data: dict[str, str]):
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=None
        )

        user_list = await get_next_user(call.from_user.id)
        random_user = secrets.choice(user_list)
        await state.set_state("finding")
        try:
            await create_questionnaire(form_owner=random_user, chat_id=call.from_user.id)
            await state.reset_data()
        except IndexError:
            await call.answer(_("На данный момент у нас нет подходящих анкет для вас"))
            await state.reset_data()


class ChooseReportReason(ActionStrategy):
    async def execute(
            self,
            call: CallbackQuery,
            state: FSMContext,
            callback_data: dict[str, str]
    ):
        await state.reset_state()
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        target_id = int(callback_data["target_id"])
        await call.message.answer(
            text=_("<u>Выберите причину жалобы:</u>"),
            reply_markup=await report_menu_keyboard(telegram_id=target_id)
        )


class SendReport(ActionStrategy):
    async def execute(
            self,
            call: CallbackQuery,
            state: FSMContext,
            callback_data: dict[str, str]
    ):
        target_id = int(callback_data["target_id"])
        text = _(
            "Жалоба от пользователя: <code>[@{username}</code> | <code>{tg_id}</code>]\n\n"
            "На пользователя: <code>[{owner_id}]</code>\n"
            "Причина жалобы: <code>{reason}</code>"
        ).format(
            username=call.from_user.username,
            tg_id=call.from_user.id,
            owner_id=target_id,
            reason=await get_report_reason(call)
        )

        await create_questionnaire(
            form_owner=target_id,
            chat_id=load_config().tg_bot.moderate_chat,
            report_system=True,
            add_text=text
        )
        await asyncio.sleep(1)
