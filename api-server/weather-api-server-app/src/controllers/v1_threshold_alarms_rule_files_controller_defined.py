"""
Threshold rule CRUD controller — stores rules in OpenSearch (index: threshold-rules).
"""

import os
import json
import yaml
import logging

from functools import wraps
from flask import jsonify, make_response
from opensearch_db import opensearch_client as se
from opensearchpy.exceptions import NotFoundError

from swagger_server.models.v1_error import V1Error
from swagger_server import util, models

log_level = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger("Threshold Controller")
fmt = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(fmt)
logger.addHandler(handler)
logger.setLevel(log_level)
logger.propagate = False

vm_threshold_enable = os.getenv("THRESHOLD_ENABLE", "false").lower() == "true"

RULES_INDEX = "threshold-rules"


def check_threshold_enabled(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not vm_threshold_enable:
            return make_response(jsonify(V1Error(405, "Method Not Allowed")), 405)
        return func(*args, **kwargs)
    return wrapper


def _get_client():
    return se.get_opensearch_client()


def _close(client):
    try:
        if client:
            se.close_opensearch_client(client)
    except Exception:
        pass


# ── CRUD endpoints ────────────────────────────────────────────────

@check_threshold_enabled
def list_rule_files():
    """List all threshold rule documents stored in OpenSearch."""
    client = None
    try:
        client = _get_client()
        resp = client.search(index=RULES_INDEX, body={"query": {"match_all": {}}, "size": 1000})
        results = [{"name": hit["_id"], "rules": hit["_source"]} for hit in resp["hits"]["hits"]]
        return make_response(jsonify(results), 200)
    except NotFoundError:
        return make_response(jsonify([]), 200)
    except Exception as err:
        logger.error(f"Error listing rules: {err}")
        return make_response(jsonify(V1Error(500, f"Error listing rules: {err}")), 500)
    finally:
        _close(client)


@check_threshold_enabled
def upload_rule_file(body, file_name):
    """Create a new threshold rule document in OpenSearch."""
    if not body:
        return make_response(jsonify(V1Error(412, "Body is required")), 412)

    content = _parse_body(body)
    if isinstance(content, tuple):
        return content  # error response

    client = None
    try:
        client = _get_client()
        # Check if already exists
        try:
            client.get(index=RULES_INDEX, id=file_name)
            return make_response(jsonify(V1Error(400, "Rule already exists")), 400)
        except NotFoundError:
            pass

        client.index(index=RULES_INDEX, id=file_name, body=json.dumps(content))
        return make_response(jsonify({"code": 201, "message": "Rule created successfully"}), 201)
    except Exception as err:
        logger.error(f"Error creating rule: {err}")
        return make_response(jsonify(V1Error(500, f"Error creating rule: {err}")), 500)
    finally:
        _close(client)


@check_threshold_enabled
def get_rule_file(file_name):
    """Get a threshold rule document from OpenSearch."""
    client = None
    try:
        client = _get_client()
        doc = client.get(index=RULES_INDEX, id=file_name)
        return make_response(jsonify({"name": file_name, "rules": doc["_source"]}), 200)
    except NotFoundError:
        return make_response(jsonify(V1Error(404, "Rule not found")), 404)
    except Exception as err:
        logger.error(f"Error getting rule: {err}")
        return make_response(jsonify(V1Error(500, f"Error: {err}")), 500)
    finally:
        _close(client)


@check_threshold_enabled
def update_rule_file(body, file_name):
    """Update an existing threshold rule document in OpenSearch."""
    if not body:
        return make_response(jsonify(V1Error(412, "Body is required")), 412)

    content = _parse_body(body)
    if isinstance(content, tuple):
        return content

    client = None
    try:
        client = _get_client()
        # Must exist to update
        try:
            client.get(index=RULES_INDEX, id=file_name)
        except NotFoundError:
            return make_response(jsonify(V1Error(404, "Rule not found")), 404)

        client.index(index=RULES_INDEX, id=file_name, body=json.dumps(content))
        return make_response(jsonify({"code": 200, "message": "Rule updated successfully"}), 200)
    except Exception as err:
        logger.error(f"Error updating rule: {err}")
        return make_response(jsonify(V1Error(500, f"Error: {err}")), 500)
    finally:
        _close(client)


@check_threshold_enabled
def delete_rule_file(file_name):
    """Delete a threshold rule document from OpenSearch."""
    client = None
    try:
        client = _get_client()
        client.delete(index=RULES_INDEX, id=file_name)
        return make_response(jsonify({"code": 200, "message": "Rule deleted successfully"}), 200)
    except NotFoundError:
        return make_response(jsonify(V1Error(404, "Rule not found")), 404)
    except Exception as err:
        logger.error(f"Error deleting rule: {err}")
        return make_response(jsonify(V1Error(500, f"Error: {err}")), 500)
    finally:
        _close(client)


# ── Helpers ───────────────────────────────────────────────────────

def _parse_body(body):
    """Parse YAML or JSON body into a dict. Returns error tuple on failure."""
    try:
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        if isinstance(body, str):
            return yaml.safe_load(body)
        if isinstance(body, dict):
            return body
        return json.loads(body)
    except Exception as exc:
        logger.error(f"Failed to parse body: {exc}")
        return make_response(jsonify(V1Error(400, f"Invalid content: {exc}")), 400), 400
