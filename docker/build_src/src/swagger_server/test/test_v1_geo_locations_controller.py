# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.v1_error import V1Error  # noqa: E501
from swagger_server.models.v1_geo_location import V1GeoLocation  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV1GeoLocationsController(BaseTestCase):
    """V1GeoLocationsController integration test stubs"""

    def test_list_geo_locations(self):
        """Test case for list_geo_locations

        List all the Geo Location supported by Weather Watch application
        """
        query_string = [('pincode', 'pincode_example'),
                        ('state', 'state_example'),
                        ('district', 'district_example'),
                        ('limit', 100)]
        response = self.client.open(
            '/v1/geo-locations',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
