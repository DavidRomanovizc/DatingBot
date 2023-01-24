from typing import NoReturn, Union

from aiogram import Bot
from aiogram.types import CallbackQuery

from keyboards.inline.poster_inline import create_moderate_ik, event_settings_keyboard, view_event_keyboard, \
    cancel_event_keyboard
from loader import _


class TemplateEvent:

    def __init__(self) -> NoReturn:
        self.message_for_event = _("<b>{}</b> \n" +
                                   "Когда: {} \n" +
                                   "Где: {} \n\n" +
                                   "{}")

    def template_event(self) -> str:
        return self.message_for_event

    async def send_event_message(
            self, text: dict[str, Union[str, str, int]], bot: Bot, chat_id: int,
            moderate: Union[bool, None] = None, call: Union[CallbackQuery, None] = None,
            view_event: Union[bool, None] = None
    ) -> NoReturn:
        msg = self.template_event().format(text["title"], text["date"], text["place"], text["description"])
        if moderate:
            await bot.send_photo(chat_id=chat_id, caption=msg, photo=text["photo_id"],
                                 reply_markup=await create_moderate_ik(str(text["telegram_id"])))
        if not moderate and view_event is None:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_photo(chat_id=chat_id, caption=msg, photo=text["photo_id"],
                                 reply_markup=await event_settings_keyboard())
        if view_event:
            await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            await bot.send_photo(chat_id=chat_id, caption=msg, photo=text["photo_id"],
                                 reply_markup=await view_event_keyboard(str(text["telegram_id"])))

    async def send_event_list(self, text: dict[str, Union[str, str, int]], call: CallbackQuery, telegram_id: int,
                              bot: Bot):
        msg = self.template_event().format(text["title"], text["date"], text["place"], text["description"])
        await bot.delete_message(chat_id=telegram_id, message_id=call.message.message_id)
        await call.message.answer_photo(photo=text["photo_id"], caption=msg,
                                        reply_markup=await cancel_event_keyboard(str(text["telegram_id"])))


ME = TemplateEvent()
