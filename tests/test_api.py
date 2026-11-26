from unittest.mock import MagicMock, patch

from src.api import AeroplanesAPI


@patch("requests.get")
def test_get_country_coordinates_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"boundingbox": ["10.0", "20.0", "30.0", "40.0"]}
    ]
    mock_get.return_value = mock_response

    api = AeroplanesAPI()
    coords = api.get_country_coordinates("TestCountry")

    assert coords == (10.0, 20.0, 30.0, 40.0)


@patch("requests.get")
def test_get_country_coordinates_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    api = AeroplanesAPI()
    coords = api.get_country_coordinates("UnknownCountry")

    assert coords is None
