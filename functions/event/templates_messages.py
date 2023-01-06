from typing import NoReturn, Union

from aiogram import Bot
from aiogram.types import CallbackQuery

from keyboards.inline.poster_inline import create_moderate_ik, event_settings_keyboard
from loader import _


class TemplateEvent:

    def __init__(self) -> NoReturn:
        self.message_for_event = _("<b>{}</b> \n" +
                                   "Когда: {} \n" +
                                   "Где: {} \n\n" +
                                   "{}")

    def template_event(self) -> str:
        return self.message_for_event

    async def send_event_message(self, text: dict[str, Union[str, str, int]], bot: Bot, chat_id: int,
                                 moderate: bool, call: Union[CallbackQuery, None] = None) -> NoReturn:
        msg = self.template_event().format(text["title"], text["date"], text["place"], text["description"])
        if moderate:
            await bot.send_photo(chat_id=chat_id, caption=msg, photo=text["photo_id"],
                                 reply_markup=await create_moderate_ik(str(text['telegram_id'])))
        if not moderate:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_photo(chat_id=chat_id, caption=msg, photo=text["photo_id"],
                                 reply_markup=await event_settings_keyboard())


ME = TemplateEvent()
