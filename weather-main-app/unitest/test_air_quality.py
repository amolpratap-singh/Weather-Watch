import pytest
from unittest.mock import MagicMock, patch
from src.weatherapp.handler.air_quality import AirQualityIndex

@pytest.fixture
def mocked_aqi():
    return AirQualityIndex("thread_name", 1)

def test_set_aqi_data_successful(mocked_aqi, caplog):
    with patch.object(mocked_aqi.opensearchdb, 'read_doc', return_value={"lat": 12.34, "lon": 56.78}), \
         patch.object(mocked_aqi, '_set_aqi_body_data', return_value={"location": {"lat": 12.34, "lon": 56.78}}), \
         patch('src.weatherapp.handler.air_quality.requests.get') as mocked_get:
        
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {"list": [{"main": {"aqi": 50}, "components": "", "dt": 123456789}]}
        
        mocked_aqi._set_aqi_data(123456)
        
        assert "AQI Requests been sent towards API" in caplog.text
        assert "Pushing Data" in caplog.text
        assert "AQI data is not present in the history data" in caplog.text

def test_set_aqi_data_no_lat_lon(mocked_aqi, caplog):
    with patch.object(mocked_aqi.opensearchdb, 'read_doc', return_value={}):
        mocked_aqi._set_aqi_data(123456)
        
        assert "doesn't contain latitude and longitude skipping the task" in caplog.text

def test_set_aqi_data_http_error(mocked_aqi, caplog):
    with patch.object(mocked_aqi.opensearchdb, 'read_doc', return_value={"lat": 12.34, "lon": 56.78}), \
         patch('src.weatherapp.handler.air_quality.requests.get') as mocked_get:
        
        mocked_get.return_value.status_code = 404
        
        with pytest.raises(Exception) as excinfo:
            mocked_aqi._set_aqi_data(123456)
        
        assert "http error while connecting" in caplog.text
        assert "Error occured while connecting" in caplog.text
        assert "Error occured while connecting" in str(excinfo.value)

def test_set_aqi_data_connection_error(mocked_aqi, caplog):
    with patch.object(mocked_aqi.opensearchdb, 'read_doc', return_value={"lat": 12.34, "lon": 56.78}), \
         patch('src.weatherapp.handler.air_quality.requests.get') as mocked_get:
        
        mocked_get.side_effect = ConnectionError("Connection error")
        
        with pytest.raises(ConnectionError) as excinfo:
            mocked_aqi._set_aqi_data(123456)
        
        assert "Error while connecting" in caplog.text
        assert "Error while connecting" in str(excinfo.value)

def test_set_aqi_data_timeout_error(mocked_aqi, caplog):
    with patch.object(mocked_aqi.opensearchdb, 'read_doc', return_value={"lat": 12.34, "lon": 56.78}), \
         patch('src.weatherapp.handler.air_quality.requests.get') as mocked_get:
        
        mocked_get.side_effect = TimeoutError("Timeout error")
        
        with pytest.raises(TimeoutError) as excinfo:
            mocked_aqi._set_aqi_data(123456)
        
        assert "Time out error occur while connecting" in caplog.text
        assert "Time out error occur while connecting" in str(excinfo.value)

def test_set_aqi_data_unknown_error(mocked_aqi, caplog):
    with patch.object(mocked_aqi.opensearchdb, 'read_doc', return_value={"lat": 12.34, "lon": 56.78}), \
         patch('src.weatherapp.handler.air_quality.requests.get') as mocked_get:
        
        mocked_get.side_effect = Exception("Unknown error")
        
        with pytest.raises(Exception) as excinfo:
            mocked_aqi._set_aqi_data(123456)
        
        assert "Error occured while connecting" in caplog.text
        assert "Error occured while connecting" in str(excinfo.value)
