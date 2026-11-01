from typing import Any, List


class Aeroplane:
    """Класс, описывающий самолет и его характеристики."""

    def __init__(self, callsign: str, origin_country: str, velocity: float, baro_altitude: float, icao24: str = ""):
        self.callsign = callsign.strip()
        self.origin_country = origin_country
        self.velocity = self._validate_number(velocity, "velocity")
        self.baro_altitude = self._validate_number(baro_altitude, "baro_altitude")
        self.icao24 = icao24

    @staticmethod
    def _validate_number(value: Any, field_name: str) -> float:
        """Валидация числовых данных (скорость, высота)."""
        try:
            float_val = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Некорректное значение для {field_name}.")

        if float_val < 0:
            raise ValueError(f"{field_name} не может быть отрицательной.")

        return float_val

    @classmethod
    def cast_to_object_list(cls, api_data: List[List[Any]]) -> List['Aeroplane']:
        """Преобразование сырых данных из OpenSky API в список объектов Aeroplane."""
        aeroplanes = []
        if not api_data:
            return aeroplanes

        for item in api_data:
            # Согласно документации OpenSky API:
            # index 1 - callsign, index 2 - origin_country, index 7 - baro_altitude, index 9 - velocity
            try:
                callsign = item[1] if item[1] else "Unknown"
                country = item[2] if item[2] else "Unknown"
                altitude = item[7] if item[7] is not None else 0.0
                velocity = item[9] if item[9] is not None else 0.0
                icao = item[0]
                aeroplanes.append(cls(callsign, country, velocity, altitude, icao))
            except (IndexError, ValueError):
                continue  # Пропускаем поврежденные данные
        return aeroplanes

    def __eq__(self, other: 'Aeroplane') -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity == other.velocity and self.baro_altitude == other.baro_altitude

    def __lt__(self, other: 'Aeroplane') -> bool:
        """Сравнение по высоте полета (по умолчанию для сортировки)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.baro_altitude < other.baro_altitude

    def __str__(self) -> str:
        return (f"Позывной: {self.callsign:10} | Страна: {self.origin_country:15} | "
                f"Скорость: {self.velocity:7.2f} м/с | Высота: {self.baro_altitude:8.2f} м")
