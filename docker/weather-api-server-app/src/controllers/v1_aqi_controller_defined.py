import six
import connexion
import json
from flask import jsonify, make_response

from swagger_server.models.v1_air_quality_index import V1AirQualityIndex  # noqa: E501
from swagger_server.models.v1_error import V1Error  # noqa: E501
from swagger_server import util


def list_current_air_quality_index(pincode=None, state=None, district=None, page_ref=None, limit=None, order=None, sort_by=None):  # noqa: E501
    """List the current air quality index of a location

    API used to get the list of Current Air Quality Index Information for India # noqa: E501

    :param pincode: If pincode query attribute provided, response will contain the AQI record  for that Geo Location.
    :type pincode: str
    :param state: If state query attribute provided, response will contain the AQI record  for that Geo Location.
    :type state: str
    :param district: If district query attribute provided, response will contain the AQI record  for that Geo Location.
    :type district: str
    :param limit: It display the list from the startFrom value till th value provided in the limit attribute. If limit is not provided it will provide till default  value which is 100.
    :type limit: int

    :rtype: List[V1AirQualityIndex]
    """
    
    output ={
            "dt": 2,
            "components": {
            "No2": 5.637377,
            "O3": 2.302136,
            "So2": 7.0614014,
            "pm2_5": 3.6160767,
            "Nh3": 1.4658129,
            "pm10": 9.301444,
            "NitricOxide": 5.962134,
            "Co": 6.0274563
            },
            "aqi": 0,
            "eventTime": "2000-01-23T04:56:07.000+00:00",
            "location": {
            "pincode": 1,
            "countryCode": "countryCode",
            "district": "district",
            "taluka": "taluka",
            "postOfficeName": "postOfficeName",
            "lon": 1.2315135,
            "state": "state",
            "lat": 7.386282
            },
            "epochTime": 4
        }
    
    response = make_response()
    response.data = json.dumps(output)
    return response, 200