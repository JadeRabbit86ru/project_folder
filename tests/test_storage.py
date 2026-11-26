import pytest

from src.aeroplane import Aeroplane
from src.storage import JSONSaver


@pytest.fixture
def temp_json_file(tmp_path):
    return str(tmp_path / "test_aeroplanes.json")


def test_add_and_get(temp_json_file):
    saver = JSONSaver(temp_json_file)
    a = Aeroplane("TEST1", "Germany", 200.0, 5000.0, "icao1")
    saver.add_aeroplane(a)

    saved = saver.get_aeroplanes()
    assert len(saved) == 1
    assert saved[0].callsign == "TEST1"

    # Фильтрация
    filtered = saver.get_aeroplanes({"origin_country": "Germany"})
    assert len(filtered) == 1
    filtered_empty = saver.get_aeroplanes({"origin_country": "France"})
    assert len(filtered_empty) == 0


def test_delete(temp_json_file):
    saver = JSONSaver(temp_json_file)
    a = Aeroplane("TEST1", "Germany", 200.0, 5000.0, "icao1")
    saver.add_aeroplane(a)

    assert saver.delete_aeroplane(a) is True
    assert len(saver.get_aeroplanes()) == 0
    assert saver.delete_aeroplane(a) is False
