from typing import Tuple

import aiohttp
import pytest

from data.config import load_config
from loader import client
from utils.YandexMap.api import Client
from utils.YandexMap.exceptions import UnexpectedResponse, InvalidKey, NothingFound


@pytest.mark.asyncio
async def test_request_success():
    async with aiohttp.ClientSession() as session:
        async with session.get(url="https://geocode-maps.yandex.ru/1.x/",
                               params=dict(format="json",
                                           apikey=load_config().misc.yandex_api_key, geocode="Detroit")) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, dict)
            assert "response" in data


@pytest.mark.asyncio
async def test_request_invalid_key():
    with pytest.raises(InvalidKey):
        cl = Client(api_key="invalid_key")
        await cl._request("Detroit")


@pytest.mark.asyncio
async def test_request_unexpected_response():
    with pytest.raises(UnexpectedResponse):
        cl = Client(api_key="valid_key")
        await cl._request("InvalidAddress")


@pytest.mark.asyncio
async def test_coordinates_success():
    coordinates = await client.coordinates("Detroit")
    assert isinstance(coordinates, Tuple)
    assert len(coordinates) == 2
    assert all(isinstance(coord, str) for coord in coordinates)


@pytest.mark.asyncio
async def test_address_success():
    coordinates = await client.coordinates("Detroit")
    address = await client.address(*coordinates)
    assert isinstance(address, str)


@pytest.mark.asyncio
async def test_address_nothing_found():
    with pytest.raises(NothingFound):
        await client.address("100.0", "200.0")
