# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.v1_air_quality_index import V1AirQualityIndex  # noqa: E501
from swagger_server.models.v1_error import V1Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV1AqiController(BaseTestCase):
    """V1AqiController integration test stubs"""

    def test_list_current_air_quality_index(self):
        """Test case for list_current_air_quality_index

        List the current air quality index of a location
        """
        query_string = [('pincode', 'pincode_example'),
                        ('state', 'state_example'),
                        ('district', 'district_example'),
                        ('page_ref', 'page_ref_example'),
                        ('limit', 100),
                        ('order', 1),
                        ('sort_by', 'sort_by_example')]
        response = self.client.open(
            '/v1/currentAirQualityIndex',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
