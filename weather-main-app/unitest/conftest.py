import sys
import pytest

sys.dont_write_bytecode = True


WEATHER_RESPONSE = {
    "coord": {
        "lon": 73.0617,
        "lat": 8.289
    },
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01n"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 27.82,
        "feels_like": 30.45,
        "temp_min": 27.82,
        "temp_max": 27.82,
        "pressure": 1012,
        "humidity": 71,
        "sea_level": 1012,
        "grnd_level": 1010
    },
    "visibility": 10000,
    "wind": {
        "speed": 1.8,
        "deg": 357,
        "gust": 1.58
    },
    "clouds": {
        "all": 8
    },
    "dt": 1707940674,
    "sys": {
        "sunrise": 1707960376,
        "sunset": 1708003069
    },
    "timezone": 19800,
    "id": 0,
    "name": "",
    "cod": 200
}

AQI_RESPONSE = {
    "coord": {
        "lon": 82.174,
        "lat": 21.0713
    },
    "list": [
        {
            "main": {
                "aqi": 4
            },
            "components": {
                "co": 387.19,
                "no": 0.1,
                "no2": 1.01,
                "o3": 138.76,
                "so2": 9.18,
                "pm2_5": 55.25,
                "pm10": 72.25,
                "nh3": 4.56
            },
            "dt": 1708846209
        }
    ]
}


@pytest.fixture
def weather_response():
    return WEATHER_RESPONSE

@pytest.fixture
def aqi_response():
    return AQI_RESPONSE



