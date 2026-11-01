import pytest
from src.aeroplane import Aeroplane


def test_validation_success():
    a = Aeroplane("CSN123", "China", 250.5, 10000.0)
    assert a.callsign == "CSN123"
    assert a.velocity == 250.5
    assert a.baro_altitude == 10000.0


def test_validation_negative_velocity():
    with pytest.raises(ValueError, match="не может быть отрицательной"):
        Aeroplane("CSN123", "China", -10.0, 10000.0)


def test_validation_invalid_type():
    with pytest.raises(ValueError, match="Некорректное значение"):
        Aeroplane("CSN123", "China", "fast", 10000.0)


def test_comparison():
    a1 = Aeroplane("A1", "USA", 100, 5000)
    a2 = Aeroplane("A2", "USA", 200, 10000)

    assert a1 < a2  # Сравнение по высоте
    assert not (a2 < a1)
    assert a1 != a2


def test_cast_to_object_list():
    raw_data = [
        ["icao1", "AAL123", "United States", 123, 123, 10.0, 20.0, 8000.0, False, 250.0],
        ["icao2", "UAE45", "United Arab Emirates", 123, 123, 11.0, 21.0, 9000.0, False, 300.0]
    ]
    aeroplanes = Aeroplane.cast_to_object_list(raw_data)
    assert len(aeroplanes) == 2
    assert aeroplanes[0].callsign == "AAL123"
    assert aeroplanes[1].baro_altitude == 9000.0
