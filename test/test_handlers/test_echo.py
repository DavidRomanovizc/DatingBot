from unittest.mock import (
    AsyncMock,
)

from aiogram.utils.markdown import (
    hcode,
)
import pytest

from handlers.echo_handler import (
    bot_echo,
)


@pytest.mark.asyncio
async def test_echo_handler() -> None:
    text_mock = ["Эхо без состояния.", "Сообщение: ", hcode("repeat me")]
    message_mock = AsyncMock(text=text_mock)
    await bot_echo(message=message_mock)
    message_mock.answer.assert_called_with(text_mock)
