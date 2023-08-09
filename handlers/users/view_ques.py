import random
import secrets
from abc import ABC, abstractmethod

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from functions.dating.create_forms_funcs import (
    create_questionnaire,
    rand_user_list,
    create_questionnaire_reciprocity
)
from functions.dating.get_next_user_func import get_next_user
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.questionnaires_inline import (
    action_keyboard,
    action_reciprocity_keyboard,
    user_link_keyboard
)
from loader import bot, _, dp
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
        telegram_id = call.from_user.id
        user_list = await get_next_user(telegram_id, call)
        random_user = random.choice(user_list)
        await create_questionnaire(form_owner=random_user, chat_id=telegram_id)
        await state.set_state("finding")


class StartFindingFailure(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, **kwargs):
        await call.answer(_("На данный момент у нас нет подходящих анкет для вас"))


class LikeAction(ActionStrategy):
    async def execute(self, call: CallbackQuery, state: FSMContext, callback_data: dict[str, str]):
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
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=await start_keyboard(call))
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
        await create_questionnaire_reciprocity(liker=call.from_user.id, chat_id=user_for_like, add_text="")
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

        user_list = await get_next_user(call.from_user.id, call)
        random_user = secrets.choice(user_list)
        await state.set_state("finding")
        try:
            await create_questionnaire(form_owner=random_user, chat_id=call.from_user.id)
            await state.reset_data()
        except IndexError:
            await call.answer(_("На данный момент у нас нет подходящих анкет для вас"))
            await state.reset_data()


@dp.callback_query_handler(text='find_ques')
async def handle_start_finding(call: CallbackQuery, state: FSMContext) -> None:
    user_list = await get_next_user(call.from_user.id, call)
    strategy_mapping = {
        "success": StartFindingSuccess(),
        "failure": StartFindingFailure(),
    }
    strategy = strategy_mapping.get("success" if user_list else "failure")
    await strategy.execute(call=call, state=state)


@dp.callback_query_handler(action_keyboard.filter(action=["like", "dislike", "stopped"]),
                           state='finding')
async def handle_action(call: CallbackQuery, state: FSMContext, callback_data: dict[str, str]) -> None:
    action = callback_data["action"]
    profile_id = callback_data["target_id"]
    user = await db_commands.select_user_object(telegram_id=call.from_user.id)
    viewed_profile = await db_commands.select_user_object(telegram_id=profile_id)
    await db_commands.add_profile_to_viewed(user=user, viewed_profile=viewed_profile)

    strategy_mapping = {
        "like": LikeAction(),
        "dislike": DislikeAction(),
        "stopped": StoppedAction()
    }
    strategy = strategy_mapping.get(action)
    if strategy:
        await strategy.execute(call, state, callback_data)


@dp.callback_query_handler(action_reciprocity_keyboard.filter(action=["like_reciprocity", "dislike_reciprocity"]))
async def handle_reciprocity_action(call: CallbackQuery, state: FSMContext,
                                    callback_data: dict[str, str]) -> None:
    action = callback_data['action']
    strategy_mapping = {
        "like_reciprocity": LikeReciprocity(),
        "dislike_reciprocity": DislikeReciprocity()
    }
    strategy = strategy_mapping.get(action)
    if strategy:
        await strategy.execute(call, state, callback_data)


@dp.callback_query_handler(state="*", text="go_back_to_viewing_ques")
async def handle_go_back_to_viewing(call: CallbackQuery, state: FSMContext) -> None:
    strategy = GoBackToViewing()
    # noinspection PyTypeChecker
    await strategy.execute(call, state, None)
