from datetime import datetime, timedelta
from typing import NoReturn
from unittest import mock
from unittest.mock import AsyncMock
from unittest.mock import Mock, patch

import pytest

from functions.event import extra_features
from utils.db_api import db_commands


@pytest.mark.asyncio
async def test_check_event_date_past_date() -> None:
    telegram_id = 1
    event_time = datetime.now() - timedelta(days=10)
    with patch.object(
            db_commands,
            "select_user_meetings",
            new=AsyncMock(return_value={"time_event": event_time.strftime("%d-%m-%Y")}),
    ):
        update_mock = AsyncMock()
        with patch.object(
                db_commands, "update_user_meetings_data", new=update_mock
        ) as mock:
            await extra_features.check_event_date(telegram_id)
            mock.assert_called_once_with(
                telegram_id=telegram_id,
                is_admin=False,
                verification_status=False,
                is_active=False,
            )


@pytest.mark.asyncio
async def test_check_event_date_future_date() -> None:
    telegram_id = 1
    event_time = datetime.now() + timedelta(days=10)
    with patch.object(
            db_commands,
            "select_user_meetings",
            new=AsyncMock(return_value={"time_event": event_time.strftime("%d-%m-%Y")}),
    ):
        update_mock = AsyncMock()
        with patch.object(
                db_commands, "update_user_meetings_data", new=update_mock
        ) as mock:
            await extra_features.check_event_date(telegram_id)
            mock.assert_called_once_with(
                telegram_id=telegram_id,
                is_admin=True,
                verification_status=True,
                is_active=True,
            )


@pytest.mark.asyncio
async def test_get_next_registration() -> NoReturn:
    db_command = Mock()
    db_command.select_user.return_value = {"telegram_id": 1, "events": []}
    result = await extra_features.get_next_registration(telegram_id=1)
    assert result == []


@pytest.mark.asyncio
async def test_get_next_random_event_id() -> NoReturn:
    # Mock search_event_forms() для возврата тестовых данных
    mock_event_forms = [
        {"telegram_id": 1},
        {"telegram_id": 2},
        {"telegram_id": 3},
    ]
    db_commands.search_event_forms = mock.AsyncMock(return_value=mock_event_forms)

    db_commands.check_returned_event_id = mock.AsyncMock(return_value=False)

    event_id = await extra_features.get_next_random_event_id(telegram_id=1)
    assert event_id == 2

    await db_commands.check_returned_event_id(telegram_id=1, id_of_events_seen=2)

    with pytest.raises(ValueError) as exc_info:
        await extra_features.get_next_random_event_id(telegram_id=1)
    assert str(exc_info.value) == "No upcoming events found"

    db_commands.check_returned_event_id = mock.AsyncMock(return_value=True)

    event_id = await extra_features.get_next_random_event_id(telegram_id=2)
    assert event_id == 3
