from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple

import requests


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def get_country_coordinates(
        self, country_name: str
    ) -> Optional[Tuple[float, float, float, float]]:
        """Получение boundingbox страны (юг, север, запад, восток)."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country_name: str) -> List[List[Any]]:
        """Получение информации о самолетах в воздушном пространстве страны."""
        pass


class AeroplanesAPI(AbstractAPI):
    """Класс для работы с API Nominatim и OpenSky."""

    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.headers = {"User-Agent": "AeroplaneTrackerCoursework/1.0"}

    def get_country_coordinates(
        self, country_name: str
    ) -> Optional[Tuple[float, float, float, float]]:
        params = {"q": country_name, "format": "json", "limit": 1}
        try:
            response = requests.get(
                self.nominatim_url, params=params, headers=self.headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                print(f"Страна '{country_name}' не найдена.")
                return None

            # boundingbox: [юг, север, запад, восток] -> преобразуем в float
            bbox = data[0]["boundingbox"]
            south, north, west, east = map(float, bbox)
            return south, north, west, east
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Ошибка при получении координат: {e}")
            return None

    def get_aeroplanes(self, country_name: str) -> List[List[Any]]:
        coords = self.get_country_coordinates(country_name)
        if not coords:
            return []

        south, north, west, east = coords
        params = {"lamin": south, "lomin": west, "lamax": north, "lomax": east}

        try:
            response = requests.get(self.opensky_url, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
            # Если states равно None (нет самолетов), возвращаем пустой список
            return data.get("states") or []
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении данных о самолетах: {e}")
            return []
