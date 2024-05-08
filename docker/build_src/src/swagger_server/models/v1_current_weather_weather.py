# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class V1CurrentWeatherWeather(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, feels_like: float=None, grnd_level: int=None, humidity: int=None, pressure: int=None, sea_level: int=None, temp: float=None, temp_max: float=None, temp_min: float=None):  # noqa: E501
        """V1CurrentWeatherWeather - a model defined in Swagger

        :param feels_like: The feels_like of this V1CurrentWeatherWeather.  # noqa: E501
        :type feels_like: float
        :param grnd_level: The grnd_level of this V1CurrentWeatherWeather.  # noqa: E501
        :type grnd_level: int
        :param humidity: The humidity of this V1CurrentWeatherWeather.  # noqa: E501
        :type humidity: int
        :param pressure: The pressure of this V1CurrentWeatherWeather.  # noqa: E501
        :type pressure: int
        :param sea_level: The sea_level of this V1CurrentWeatherWeather.  # noqa: E501
        :type sea_level: int
        :param temp: The temp of this V1CurrentWeatherWeather.  # noqa: E501
        :type temp: float
        :param temp_max: The temp_max of this V1CurrentWeatherWeather.  # noqa: E501
        :type temp_max: float
        :param temp_min: The temp_min of this V1CurrentWeatherWeather.  # noqa: E501
        :type temp_min: float
        """
        self.swagger_types = {
            'feels_like': float,
            'grnd_level': int,
            'humidity': int,
            'pressure': int,
            'sea_level': int,
            'temp': float,
            'temp_max': float,
            'temp_min': float
        }

        self.attribute_map = {
            'feels_like': 'feels_like',
            'grnd_level': 'grnd_level',
            'humidity': 'humidity',
            'pressure': 'pressure',
            'sea_level': 'sea_level',
            'temp': 'temp',
            'temp_max': 'temp_max',
            'temp_min': 'temp_min'
        }
        self._feels_like = feels_like
        self._grnd_level = grnd_level
        self._humidity = humidity
        self._pressure = pressure
        self._sea_level = sea_level
        self._temp = temp
        self._temp_max = temp_max
        self._temp_min = temp_min

    @classmethod
    def from_dict(cls, dikt) -> 'V1CurrentWeatherWeather':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The V1CurrentWeather_weather of this V1CurrentWeatherWeather.  # noqa: E501
        :rtype: V1CurrentWeatherWeather
        """
        return util.deserialize_model(dikt, cls)

    @property
    def feels_like(self) -> float:
        """Gets the feels_like of this V1CurrentWeatherWeather.


        :return: The feels_like of this V1CurrentWeatherWeather.
        :rtype: float
        """
        return self._feels_like

    @feels_like.setter
    def feels_like(self, feels_like: float):
        """Sets the feels_like of this V1CurrentWeatherWeather.


        :param feels_like: The feels_like of this V1CurrentWeatherWeather.
        :type feels_like: float
        """
        if feels_like is None:
            raise ValueError("Invalid value for `feels_like`, must not be `None`")  # noqa: E501

        self._feels_like = feels_like

    @property
    def grnd_level(self) -> int:
        """Gets the grnd_level of this V1CurrentWeatherWeather.


        :return: The grnd_level of this V1CurrentWeatherWeather.
        :rtype: int
        """
        return self._grnd_level

    @grnd_level.setter
    def grnd_level(self, grnd_level: int):
        """Sets the grnd_level of this V1CurrentWeatherWeather.


        :param grnd_level: The grnd_level of this V1CurrentWeatherWeather.
        :type grnd_level: int
        """
        if grnd_level is None:
            raise ValueError("Invalid value for `grnd_level`, must not be `None`")  # noqa: E501

        self._grnd_level = grnd_level

    @property
    def humidity(self) -> int:
        """Gets the humidity of this V1CurrentWeatherWeather.


        :return: The humidity of this V1CurrentWeatherWeather.
        :rtype: int
        """
        return self._humidity

    @humidity.setter
    def humidity(self, humidity: int):
        """Sets the humidity of this V1CurrentWeatherWeather.


        :param humidity: The humidity of this V1CurrentWeatherWeather.
        :type humidity: int
        """
        if humidity is None:
            raise ValueError("Invalid value for `humidity`, must not be `None`")  # noqa: E501

        self._humidity = humidity

    @property
    def pressure(self) -> int:
        """Gets the pressure of this V1CurrentWeatherWeather.


        :return: The pressure of this V1CurrentWeatherWeather.
        :rtype: int
        """
        return self._pressure

    @pressure.setter
    def pressure(self, pressure: int):
        """Sets the pressure of this V1CurrentWeatherWeather.


        :param pressure: The pressure of this V1CurrentWeatherWeather.
        :type pressure: int
        """
        if pressure is None:
            raise ValueError("Invalid value for `pressure`, must not be `None`")  # noqa: E501

        self._pressure = pressure

    @property
    def sea_level(self) -> int:
        """Gets the sea_level of this V1CurrentWeatherWeather.


        :return: The sea_level of this V1CurrentWeatherWeather.
        :rtype: int
        """
        return self._sea_level

    @sea_level.setter
    def sea_level(self, sea_level: int):
        """Sets the sea_level of this V1CurrentWeatherWeather.


        :param sea_level: The sea_level of this V1CurrentWeatherWeather.
        :type sea_level: int
        """
        if sea_level is None:
            raise ValueError("Invalid value for `sea_level`, must not be `None`")  # noqa: E501

        self._sea_level = sea_level

    @property
    def temp(self) -> float:
        """Gets the temp of this V1CurrentWeatherWeather.


        :return: The temp of this V1CurrentWeatherWeather.
        :rtype: float
        """
        return self._temp

    @temp.setter
    def temp(self, temp: float):
        """Sets the temp of this V1CurrentWeatherWeather.


        :param temp: The temp of this V1CurrentWeatherWeather.
        :type temp: float
        """
        if temp is None:
            raise ValueError("Invalid value for `temp`, must not be `None`")  # noqa: E501

        self._temp = temp

    @property
    def temp_max(self) -> float:
        """Gets the temp_max of this V1CurrentWeatherWeather.


        :return: The temp_max of this V1CurrentWeatherWeather.
        :rtype: float
        """
        return self._temp_max

    @temp_max.setter
    def temp_max(self, temp_max: float):
        """Sets the temp_max of this V1CurrentWeatherWeather.


        :param temp_max: The temp_max of this V1CurrentWeatherWeather.
        :type temp_max: float
        """
        if temp_max is None:
            raise ValueError("Invalid value for `temp_max`, must not be `None`")  # noqa: E501

        self._temp_max = temp_max

    @property
    def temp_min(self) -> float:
        """Gets the temp_min of this V1CurrentWeatherWeather.


        :return: The temp_min of this V1CurrentWeatherWeather.
        :rtype: float
        """
        return self._temp_min

    @temp_min.setter
    def temp_min(self, temp_min: float):
        """Sets the temp_min of this V1CurrentWeatherWeather.


        :param temp_min: The temp_min of this V1CurrentWeatherWeather.
        :type temp_min: float
        """
        if temp_min is None:
            raise ValueError("Invalid value for `temp_min`, must not be `None`")  # noqa: E501

        self._temp_min = temp_min
