# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.v1_current_weather import V1CurrentWeather  # noqa: E501
from swagger_server.models.v1_error import V1Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV1WeatherController(BaseTestCase):
    """V1WeatherController integration test stubs"""

    def test_list_current_weather(self):
        """Test case for list_current_weather

        List the current weather
        """
        query_string = [('pincode', 'pincode_example'),
                        ('state', 'state_example'),
                        ('district', 'district_example'),
                        ('page_ref', 'page_ref_example'),
                        ('limit', 100),
                        ('order', 1),
                        ('sort_by', 'sort_by_example')]
        response = self.client.open(
            '/v1/currentWeather',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_history_weather(self):
        """Test case for list_history_weather

        List the historical weather Information
        """
        query_string = [('pincode', 'pincode_example'),
                        ('state', 'state_example'),
                        ('district', 'district_example'),
                        ('start_time', 'start_time_example'),
                        ('end_time', 'end_time_example'),
                        ('page_ref', 'page_ref_example'),
                        ('limit', 100),
                        ('order', 1),
                        ('sort_by', 'sort_by_example')]
        response = self.client.open(
            '/v1/historyWeather',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
