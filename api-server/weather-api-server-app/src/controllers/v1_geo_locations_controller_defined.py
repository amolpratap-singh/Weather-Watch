import os
import six
import json
import logging
import connexion
import traceback

from flask import jsonify, make_response
from opensearch_db import opensearch_client as se
from opensearchpy.exceptions import NotFoundError, RequestError, ConnectionError

from swagger_server.models.v1_error import V1Error  # noqa: E501
from swagger_server.models.v1_geo_location import V1GeoLocation  # noqa: E501
from swagger_server import util
from swagger_server import models

# Logging Configuration
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger("Geo Location Controller")
format = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(format)
logger.addHandler(handler)
logger.setLevel(log_level)
logger.propagate = False


def list_geo_locations(pincode=None, state=None, district=None, limit=None, order=None, sort_by=None):  # noqa: E501
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
    
    try:
        opensearch_client = None
        limit = 10000 if limit > 10000 else limit
        order = "desc" if order is None or order == 1 else "asc"
        
        if sort_by is not None and sort_by.lower() == "state":
            sort_by = "state"
        elif sort_by is not None and sort_by.lower() == "district":
            sort_by = "district"
        else:
            sort_by = "pincode"
        
        # Opensearch Query build up
        data = {
            "sort": [{sort_by: {"order": order}}],
            "size": limit,
            "query": {"bool": {"must": list(), "filter": list()}}
        }
        
        opensearch_client = se.get_opensearch_client()
        resp = opensearch_client.search(index='geo-location', body=data)
        results = [r['_source'] for r in resp['hits']['hits']]
        total_count = resp['hits']['total']['value']
    
    except NotFoundError as err:
        logger.error(f"Geo location data not found error :{err}")
        response = make_response()
        response.content_type = 'application/json'
        response.data = json.dumps({})
        return response, 200
    except RequestError as err:
        logger.error(f"Request error :{err}")
        ise = models.V1Error(400, "could not retrieve the geo location data")
        return jsonify(ise), 400
    except ConnectionError as err:
        logger.error(f"Connection Failed :{err}")
        ise = models.V1Error(503, "Connection failed")
        return jsonify(ise), 503
    except Exception as err:
        logger.error(f"Exception cause in geo location data: {err}")
        ise = models.V1Error(500, "could not retrieve the geo location data")
        return jsonify(ise), 500
    finally:
        try:
            if opensearch_client:
                se.close_opensearch_client(opensearch_client)
        except Exception as err:
            terr = traceback.format_exc()
            logger.error(f"Exception cause while closing opensearch :{err} and traceback: {terr}")
    
    response = make_response()
    #response.headers = {'total_count': total_count, 'next': last_index}
    response.content_type = 'application/json'
    response.data = json.dumps({'locations': results, 'total': total_count})
    
    return response, 200
