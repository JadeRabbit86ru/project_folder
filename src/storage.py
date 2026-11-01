from abc import ABC, abstractmethod
import json
import os
from typing import List, Optional, Dict, Any
from src.aeroplane import Aeroplane


class AbstractStorage(ABC):
    """Абстрактный класс для работы с хранилищем данных."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        pass

    @abstractmethod
    def get_aeroplanes(self, criteria: Optional[Dict[str, Any]] = None) -> List[Aeroplane]:
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> bool:
        pass


class JSONSaver(AbstractStorage):
    """Класс для сохранения информации о самолетах в JSON-файл."""

    def __init__(self, filename: str = "data/aeroplanes.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_file(self) -> List[Dict[str, Any]]:
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read_file()
        data.append(aeroplane.__dict__)
        self._write_file(data)

    def get_aeroplanes(self, criteria: Optional[Dict[str, Any]] = None) -> List[Aeroplane]:
        data = self._read_file()
        result = []
        for item in data:
            if criteria:
                match = all(str(item.get(k, "")).lower() == str(v).lower() for k, v in criteria.items())
                if not match:
                    continue
            try:
                result.append(
                    Aeroplane(item["callsign"], item["origin_country"], item["velocity"], item["baro_altitude"],
                              item.get("icao24", "")))
            except KeyError:
                continue
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> bool:
        data = self._read_file()
        initial_len = len(data)
        # Удаляем по уникальному ключу (icao24 + callsign) или по всем атрибутам
        data = [item for item in data if not (
                item.get("icao24") == aeroplane.icao24 and
                item.get("callsign") == aeroplane.callsign
        )]
        if len(data) < initial_len:
            self._write_file(data)
            return True
        return False
