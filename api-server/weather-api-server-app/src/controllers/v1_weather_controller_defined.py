import os
import six
import json
import logging
import connexion
import traceback

from opensearch_db import opensearch_client as se
from flask import jsonify, make_response
from opensearchpy.exceptions import NotFoundError, RequestError, ConnectionError

from swagger_server.models.v1_current_weather import V1CurrentWeather  # noqa: E501
from swagger_server.models.v1_error import V1Error  # noqa: E501
from swagger_server import util
from swagger_server import models

# Logging Configuration
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger("Weather Controller")
format = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(format)
logger.addHandler(handler)
logger.setLevel(log_level)
logger.propagate = False

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
    
    try:
        opensearch_client = None
        limit = 10000 if limit > 10000 else limit
        order = "desc" if order is None or order == 1 else "asc"
        
        if sort_by is not None and sort_by.lower() == "state":
            sort_by = "location.state"
        elif sort_by is not None and sort_by.lower() == "district":
            sort_by = "location.district"
        else:
            sort_by = "epochTime"
        
        # Opensearch Query build up
        data = {
            "sort": [{sort_by: {"order": order}}],
            "size": limit,
            "_source": {"exclude": ["dt"]},
            "query": {"bool": {"must": list(), "filter": list()}}
        }
        
        if (pincode is None and state is None and district is None):
            data["query"]["bool"]["must"].append({"match_all": {}})
        
        if pincode:
            data["query"]["bool"]["must"].append({'match': {"location.pincode": pincode}})
        
        if state:
            data["query"]["bool"]["must"].append({'match': {"location.state": state}})
            
        if district:
            data["query"]["bool"]["must"].append({'match': {"location.district": district}})
        
        opensearch_client = se.get_opensearch_client()
        resp = opensearch_client.search(index='current-weather', body=data)
        results = [r['_source'] for r in resp['hits']['hits']]
        total_count = resp['hits']['total']['value']
    
    except NotFoundError as err:
        logger.error(f"Weather Data not found error :{err}")
        response = make_response()
        response.content_type = 'application/json'
        response.data = json.dumps({})
        return response, 200
    except RequestError as err:
        logger.error(f"Request error :{err}")
        ise = models.V1Error(400, "could not retrieve the aqi data")
        return jsonify(ise), 400
    except ConnectionError as err:
        logger.error(f"Connection Failed :{err}")
        ise = models.V1Error(503, "Connection failed")
        return jsonify(ise), 503
    except Exception as err:
        logger.error(f"Exception cause in current weather data: {err}")
        ise = models.V1Error(500, "could not retrieve the aqi data")
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
    response.data = json.dumps({'weather': results, 'total': total_count})
    
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
