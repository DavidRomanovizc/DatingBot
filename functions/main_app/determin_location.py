from aiogram.types import Message

from keyboards.inline.registration_inline import confirm_keyboard
from loader import _
from loader import client
from utils.db_api import db_commands
from utils.misc.AsyncObj import AsyncObj


class Location(AsyncObj):
    """
    Класс для определения и сохранения локации пользователя во время регистрации анкеты, изменения данных,
    регистрации мероприятия.
    """

    async def __ainit__(self, message: Message) -> None:
        self.markup = await confirm_keyboard()
        self.x, self.y = await client.coordinates(message.text)
        self.city = await client.address(f"{self.x}", f"{self.y}")
        self.text = _('Я нашел такой адрес:\n'
                      '<b>{city}</b>\n'
                      'Если все правильно то подтвердите').format(city=self.city)

    async def det_loc_in_registration(self, message: Message) -> None:
        await message.answer(self.text, reply_markup=self.markup)
        await db_commands.update_user_data(telegram_id=message.from_user.id, city=self.city)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_city=self.city)
        await db_commands.update_user_data(telegram_id=message.from_user.id, longitude=self.x)
        await db_commands.update_user_data(telegram_id=message.from_user.id, latitude=self.y)

    async def det_loc_in_filters(self, message: Message) -> None:
        await message.answer(self.text, reply_markup=self.markup)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_city=self.city)

    async def det_loc_in_event(self, message: Message) -> None:
        await message.answer(self.text, reply_markup=self.markup)
        await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, venue=self.city)

    async def det_loc_in_filters_event(self, message: Message) -> None:
        await message.answer(self.text, reply_markup=self.markup)
        await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, need_location=self.city)
