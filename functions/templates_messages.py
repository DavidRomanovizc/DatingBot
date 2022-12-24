from typing import NoReturn, Union

from aiogram import Bot

from data.config import load_config
from keyboards.inline.poster_inline import create_moderate_ik
from loader import _


class ModerateEvent:

    def __init__(self) -> NoReturn:
        self.message_for_event = _("<b>{}</b> \n" +
                                   "Когда: {} \n" +
                                   "Где: {} \n" +
                                   "{}")

    def template_event(self) -> str:
        return self.message_for_event

    async def send_moderate_message(self, text: dict[str, Union[str, str, int]], bot: Bot) -> NoReturn:
        msg = self.template_event().format(text["title"], text["date"], text["place"], text["description"])
        await bot.send_photo(chat_id=load_config().tg_bot.moderate_chat, caption=msg, photo=text["photo_id"],
                             reply_markup=await create_moderate_ik(str(text['telegram_id'])))


ME = ModerateEvent()
