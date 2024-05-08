import connexion
import six

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
    :param page_ref: Pagination Reference Index
    :type page_ref: str
    :param limit: It display the list from the startFrom value till th value provided in the limit attribute. If limit is not provided it will provide till default  value which is 100.
    :type limit: int
    :param order: The response order will be based on the value passed. ascending(0) or descending(1)
    :type order: int
    :param sort_by: The response would be sorted based on one of the attribute passed. Attributes are : eventTime, state or district.
    :type sort_by: str

    :rtype: List[V1AirQualityIndex]
    """
    return 'do some magic!'
