import pytest

from unittest.mock import MagicMock, patch
from src.weatherapp.opensearchdb.opensearchclient import OpenSearchDB
from src.weatherapp.handler.geo_location import GeoLocation


@pytest.fixture
def mocked_geolocation():
    return GeoLocation()

@pytest.fixture
def mock_opensearchdb():
    return MagicMock(spec=OpenSearchDB)

def test_read_input_file(mocked_geolocation, monkeypatch):
    test_data = [{"pincode": "123456", "taluk": "Taluk1", "districtName": "District1", "stateName": "State1", "officeName": "Office1"}]
    mock_open = MagicMock(return_value=test_data)
    monkeypatch.setattr('builtins.open', mock_open)
    data = mocked_geolocation.read_input_file()
    assert data == test_data