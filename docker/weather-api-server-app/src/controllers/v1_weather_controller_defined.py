import six
import connexion

from flask import jsonify, make_response

from swagger_server.models.v1_current_weather import V1CurrentWeather  # noqa: E501
from swagger_server.models.v1_error import V1Error  # noqa: E501
from swagger_server import util


def list_current_weather(pincode=None, state=None, district=None, page_ref=None, limit=None, order=None, sort_by=None):  # noqa: E501
    """List the current weather

    API used to get the list of Current Weather Information for India # noqa: E501

    :param pincode: If pincode query attribute provided, response will contain the weather record  for that Geo Location.
    :type pincode: str
    :param state: If state query attribute provided, response will contain the weather record  for that Geo Location.
    :type state: str
    :param district: If district query attribute provided, response will contain the weather record  for that Geo Location.
    :type district: str
    :param limit: It display the list from the startFrom value till th value provided in the limit attribute. If limit is not provided it will provide till default  value which is 100.
    :type limit: int

    :rtype: List[V1CurrentWeather]
    """
    
    response = make_response()
    response.data = list()
    return response, 200


def list_history_weather(pincode=None, state=None, district=None, start_time=None, end_time=None, page_ref=None, limit=None, order=None, sort_by=None):  # noqa: E501
    """List the historical weather Information

    API used to get the list of historical Weather Information for India # noqa: E501

    :param pincode: If pincode query attribute provided, response will contain the weather record  for that Geo Location.
    :type pincode: str
    :param state: If state query attribute provided, response will contain the weather record  for that Geo Location.
    :type state: str
    :param district: If district query attribute provided, response will contain the weather record  for that Geo Location.
    :type district: str
    :param limit: It display the list from the startFrom value till th value provided in the limit attribute. If limit is not provided it will provide till default  value which is 100.
    :type limit: int
    :param start_time: Timestamp in epoch format. Filters the weather record that occurred between start time and end time, inclusive of end time.
    :type start_time: str
    :param end_time: Timestamp in epoch format. Filters the weather record that occurred between start time and end time, inclusive of end time.
    :type end_time: str

    :rtype: List[V1CurrentWeather]
    """
    
    response = make_response()
    response.data = list()
    return response, 200
