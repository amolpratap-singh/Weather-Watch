import connexion
import six

from swagger_server.models.v1_error import V1Error  # noqa: E501
from swagger_server.models.v1_geo_location import V1GeoLocation  # noqa: E501
from swagger_server import util


def list_geo_locations(pincode=None, state=None, district=None, limit=None):  # noqa: E501
    """List all the Geo Location supported by Weather Watch application

    API used to get the list of Geo Location Information supported  by Weather Watch application # noqa: E501

    :param pincode: If pincode query attribute provided, response will contain the record  for that Geo Location.
    :type pincode: str
    :param state: If state query attribute provided, response will contain the record  for that Geo Location.
    :type state: str
    :param district: If district query attribute provided, response will contain the record  for that Geo Location.
    :type district: str
    :param limit: It display the list from the startFrom value till th value provided in the limit attribute. If limit is not provided it will provide till default  value which is 100.
    :type limit: int

    :rtype: List[V1GeoLocation]
    """
    return 'do some magic!'
