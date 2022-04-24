from typing import Tuple

import requests

from .exceptions import InvalidKey, NothingFound, UnexpectedResponse


class Client:
    __slots__ = ("api_key",)

    api_key: str

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _request(self, address: str) -> dict:
        response = requests.get(
            "https://geocode-maps.yandex.ru/1.x/",
            params=dict(format="json", apikey=self.api_key, geocode=address),
        )

        if response.status_code == 200:
            return response.json()["response"]
        elif response.status_code == 403:
            raise InvalidKey()
        else:
            raise UnexpectedResponse(
                f"status_code={response.status_code}, body={response.content}"
            )

    def coordinates(self, address: str) -> Tuple:
        """Fetch coordinates (longitude, latitude) for passed address."""
        data = self._request(address)["GeoObjectCollection"]["featureMember"]

        if not data:
            raise NothingFound(f'Nothing found for "{address}" not found')

        coordinates = data[0]["GeoObject"]["Point"]["pos"]  # type: str
        longitude, latitude = tuple(coordinates.split(" "))

        return longitude, latitude

    def address(self, longitude, latitude) -> str:
        """Fetch address for passed coordinates."""
        got = self._request(f"{longitude},{latitude}")
        data = got["GeoObjectCollection"]["featureMember"]

        if not data:
            raise NothingFound(f'Nothing found for "{longitude} {latitude}"')

        return data[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
