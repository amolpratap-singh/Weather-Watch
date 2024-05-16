import logging
import pytest
from unittest.mock import MagicMock, patch
from src.weatherapp.handler.geo_location import GeoLocation
from src.weatherapp.handler.weather_data import WeatherData
from src.weatherapp.handler.air_quality import AirQualityIndex
from src.weatherapp.handler.forecast_news import ForeCastNews
from src.weatherapp.handler.weather_engine import WeatherEngine

@pytest.fixture
def mocked_weather_engine():
    return WeatherEngine()

def test_start_successful(mocked_weather_engine, caplog):
    with patch.object(GeoLocation, 'update_geolocation', return_value=True):
        with patch.object(GeoLocation, 'update_lat_lon_db') as mock_update_lat_lon_db:
            with patch.object(WeatherEngine, 'launch_threads') as mock_launch_threads:
                mocked_weather_engine.start()
                assert "Weather Engine Initiated" in caplog.text
                assert "Threads allocated to Main" in caplog.text
                assert "Main thread Process Completed" in caplog.text
                mock_update_lat_lon_db.assert_called_once()
                mock_launch_threads.assert_called_once()

def test_start_failed(mocked_weather_engine, caplog):
    with patch.object(GeoLocation, 'update_geolocation', return_value=False):
        with patch.object(GeoLocation, 'update_lat_lon_db') as mock_update_lat_lon_db:
            with patch.object(WeatherEngine, 'launch_threads') as mock_launch_threads:
                mocked_weather_engine.start()
                assert "Weather Engine Initiated" in caplog.text
                assert "Threads Not launched due to issue in update of location in Opensearch" in caplog.text
                assert "Main thread Process Completed" not in caplog.text
                mock_update_lat_lon_db.assert_not_called()
                mock_launch_threads.assert_not_called()

def test_launch_threads(mocked_weather_engine, caplog):
    with patch.object(WeatherData, 'start') as mock_weather_data_start:
        with patch.object(AirQualityIndex, 'start') as mock_aqi_start:
            with patch.object(ForeCastNews, 'start') as mock_forecast_news_start:
                mocked_weather_engine.launch_threads()
                assert "Inititalizing of thread" in caplog.text
                assert "Starting of Threads" in caplog.text
                assert "Threads allocated to Main" in caplog.text
                assert "Main thread Process Completed" in caplog.text
                mock_weather_data_start.assert_called_once()
                mock_aqi_start.assert_called_once()
                mock_forecast_news_start.assert_called_once()
