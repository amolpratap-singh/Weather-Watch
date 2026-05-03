import os
import json
import logging
import traceback

from opensearch_db import opensearch_client as se
from flask import jsonify, make_response
from opensearchpy.exceptions import NotFoundError, RequestError, ConnectionError

log_level = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger("Alerts Controller")
fmt = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(fmt)
logger.addHandler(handler)
logger.setLevel(log_level)
logger.propagate = False

ALERTS_INDEX = "weather-alerts"


def list_alerts(severity=None, alert_type=None, status=None, limit=None, order=None):
    """List threshold alerts from OpenSearch with optional filters."""
    client = None
    try:
        limit = limit if limit and limit <= 10000 else 100
        order = "desc" if order is None or order == 1 else "asc"

        must = []
        if severity:
            must.append({"match": {"severity": severity}})
        if alert_type:
            must.append({"match": {"alertType": alert_type}})
        if status:
            must.append({"match": {"status": status}})
        if not must:
            must.append({"match_all": {}})

        data = {
            "sort": [{"epochTime": {"order": order}}],
            "size": limit,
            "query": {"bool": {"must": must}},
        }

        client = se.get_opensearch_client()
        resp = client.search(index=ALERTS_INDEX, body=data)
        results = [r["_source"] for r in resp["hits"]["hits"]]
        total = resp["hits"]["total"]["value"]

    except NotFoundError:
        response = make_response()
        response.content_type = "application/json"
        response.data = json.dumps({"alerts": [], "total": 0})
        return response, 200
    except ConnectionError as err:
        logger.error(f"Connection Failed: {err}")
        return jsonify({"code": 503, "message": "Connection failed"}), 503
    except Exception as err:
        logger.error(f"Error fetching alerts: {err}")
        return jsonify({"code": 500, "message": "Could not retrieve alerts"}), 500
    finally:
        try:
            if client:
                se.close_opensearch_client(client)
        except Exception:
            pass

    response = make_response()
    response.content_type = "application/json"
    response.data = json.dumps({"alerts": results, "total": total})
    return response, 200
