from abc import ABC, abstractmethod
from typing import Type

from aiogram.types import Message

from keyboards.inline.registration_inline import confirm_keyboard
from loader import _, logger
from loader import client
from utils.YandexMap.exceptions import NothingFound
from utils.db_api import db_commands
from utils.misc.AsyncObj import AsyncObj


class UserDataUpdateStrategy(ABC):
    @abstractmethod
    async def update_user_data(self: "Location", message: Message):
        pass


class Location(AsyncObj):
    """
    Класс для определения и сохранения локации пользователя
    в различных сценариях.
    """

    async def __ainit__(self, message: Message, strategy: Type[UserDataUpdateStrategy]) -> None:
        self.markup = await confirm_keyboard()
        self.x, self.y = await client.coordinates(message.text)
        self.city = await client.address(f"{self.x}", f"{self.y}")
        self.text = _('Я нашел такой адрес:\n'
                      '<b>{city}</b>\n'
                      'Если все правильно, то подтвердите').format(city=self.city)
        self.strategy = strategy
        self.message = message

    async def det_loc(self) -> None:
        if self.city is None:
            raise NothingFound
        else:
            await self.message.answer(
                self.text,
                reply_markup=self.markup
            )
            try:
                await self.strategy.update_user_data(self, message=self.message)
            except TypeError:
                logger.info("Error in det_loc")


class RegistrationStrategy(UserDataUpdateStrategy):
    async def update_user_data(self: Location, message: Message):
        await db_commands.update_user_data(
            telegram_id=message.from_user.id,
            city=self.city,
            need_city=self.city,
            longitude=self.x,
            latitude=self.y
        )


class FiltersStrategy(UserDataUpdateStrategy):
    async def update_user_data(self: Location, message: Message):
        await db_commands.update_user_data(
            telegram_id=message.from_user.id,
            need_city=self.city
        )


class EventStrategy(UserDataUpdateStrategy):
    async def update_user_data(self: Location, message: Message):
        await db_commands.update_user_meetings_data(
            telegram_id=message.from_user.id,
            venue=self.city
        )


class EventFiltersStrategy(UserDataUpdateStrategy):
    async def update_user_data(self: Location, message: Message):
        await db_commands.update_user_meetings_data(
            telegram_id=message.from_user.id,
            need_location=self.city
        )
