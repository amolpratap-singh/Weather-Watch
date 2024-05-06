import connexion
import six

from swagger_server.models.v1_air_quality_index import V1AirQualityIndex  # noqa: E501
from swagger_server.models.v1_error import V1Error  # noqa: E501
from swagger_server import util


def list_current_air_quality_index(pincode=None, state=None, district=None, limit=None):  # noqa: E501
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
    return 'do some magic!'


def list_history_weather(pincode=None, state=None, district=None, limit=None, start_time=None, end_time=None):  # noqa: E501
    """List the historical AQI Information

    API used to get the list of historical AQI Information for India # noqa: E501

    :param pincode: If pincode query attribute provided, response will contain the AQI record  for that Geo Location.
    :type pincode: str
    :param state: If state query attribute provided, response will contain the AQI record  for that Geo Location.
    :type state: str
    :param district: If district query attribute provided, response will contain the AQI record  for that Geo Location.
    :type district: str
    :param limit: It display the list from the startFrom value till th value provided in the limit attribute. If limit is not provided it will provide till default  value which is 100.
    :type limit: int
    :param start_time: Timestamp in epoch format. Filters the weather record that occurred between start time and end time, inclusive of end time.
    :type start_time: str
    :param end_time: Timestamp in epoch format. Filters the weather record that occurred between start time and end time, inclusive of end time.
    :type end_time: str

    :rtype: List[V1AirQualityIndex]
    """
    return 'do some magic!'
