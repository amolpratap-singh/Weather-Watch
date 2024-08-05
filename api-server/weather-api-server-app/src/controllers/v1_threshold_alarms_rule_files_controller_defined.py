import os
import re
import json
import yaml
import connexion
import sys
import traceback
import logging

from flask import jsonify, make_response, request, send_file


from swagger_server.models.v1_error import V1Error  # noqa: E501
from swagger_server.models.v1alarm_rule import V1alarmRule  # noqa: E501
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

# Defined filename validation regex pattern
filename_pattern = re.compile(r'^(?!\s)([^<>:;,?"*|/\\\s]{1,31})$')

# Mountpath for file system
pvc_mount_path = "/tmp"


def upload_rule_file(body, file_name):  # noqa: E501
    """Update threshold alarms rule file

    This API is used to update the threshold alarms rule file for existing file. # noqa: E501

    :param body:
    :type body: dict | bytes
    :param file_name:
    :type file_name: str

    :rtype: None
    """

    logger.info(f"file name provided: {file_name}")
    
    # Validate the filename
    if not filename_pattern.match(file_name):
        v1error = V1Error(400, "Invalid name of file provided")
        resp = make_response(jsonify(v1error), v1error.code)
        return resp, resp.status_code

    if not body:
        v1error = V1Error(412, "Body is required")
        resp = make_response(jsonify(v1error), v1error.code)
        return resp, resp.status_code

    if connexion.request.mimetype == 'application/x-yml':
        
        # Check for the file already exists or not
        file_path = os.path.join(pvc_mount_path, file_name)
        if os.path.exists(file_path):
            v1error = V1Error(400, "Threshold alarm rule file already exists")
            resp = make_response(jsonify(v1error), v1error.code)
            return resp, resp.status_code
         
        try:
            # Decode the binary data to a string
            yaml_content_str = body.decode('utf-8')
            yaml_content = yaml.safe_load(yaml_content_str)
        except yaml.YAMLError as exc:
            ex_type, ex_val, tb = sys.exc_info()
            print(f"exception cause in update status:{ex_type} and {ex_val}")
            traceback.print_tb(tb)
            v1error = V1Error(400, "Invalid YAML content")
            resp = make_response(jsonify(v1error), v1error.code)
            return resp, resp.status_code
        
    try:
        # Convert the parsed dictionary to the model
        v1_alarm_rule = V1alarmRule.from_dict(yaml_content)
        
        # Manual validation for required fields
        file_validation(v1_alarm_rule)
    except ValueError as exc:
        v1error = V1Error(400, f"Content not provided in proper format due to{exc}")
        resp = make_response(jsonify(v1error), v1error.code)
        return resp, resp.status_code
    
     # Save the file to the PVC (Assuming the PVC is mounted at /mnt/pvc)
    file_path = os.path.join(pvc_mount_path, file_name)
    with open(file_path, 'w') as f:
        f.write(yaml_content_str)

    resp = make_response()
    resp.content_type = 'application/json'
    resp.data = json.dumps({"code": 201, "message": "File uploaded successfully"})
    return resp, 201


def get_rule_file(file_name):  # noqa: E501
    """Get Threshold alarm or record rule file content

     # noqa: E501

    :param file_name:
    :type file_name: str

    :rtype: V1alarmRule
    """
    
    if not filename_pattern.match(file_name):
        v1error = {"code": 400, "message": "Invalid file name provided"}
        return make_response(jsonify(v1error), 400)
    
    file_path = os.path.join(pvc_mount_path, file_name)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        v1error = V1Error(404, "Threshold alarm rule file not found")
        return make_response(jsonify(v1error), v1error.code)

    try:
        return send_file(file_path, mimetype='application/x-yml', as_attachment=True, 
                         download_name=file_name)
    except Exception as exc:
        v1error = V1Error(500, f"Error while retrieving file: {exc}")
        return make_response(jsonify(v1error), v1error.code)


def list_rule_files():  # noqa: E501
    """List of threshold alarms rule files

    This API is used to get list of all threshold alarms and record rule files provided by the user. # noqa: E501


    :rtype: List[str]
    """
    
    try:
        # List all files in the PVC mount path
        files = [f for f in os.listdir(pvc_mount_path) if os.path.isfile(os.path.join(pvc_mount_path, f))]
    except Exception as exc:
        v1error = V1Error(500, "Error listing files: {}".format(exc))
        return make_response(jsonify(v1error), v1error.code)

    resp = make_response()
    resp.content_type = 'application/json'
    resp.data = json.dumps(files)
    return resp, 200


def update_rule_file(body, file_name):  # noqa: E501
    """Update threshold alarms rule file

    This API is used to update the threshold alarms rule file for existing file. # noqa: E501

    :param body:
    :type body: dict | bytes
    :param file_name:
    :type file_name: str

    :rtype: None
    """
    
    print(f"file name provided: {file_name}")
    # Validate the filename
    if not filename_pattern.match(file_name):
        v1error = V1Error(400, "Invalid name of file provided")
        resp = make_response(jsonify(v1error), v1error.code)
        return resp, resp.status_code

    if not body:
        v1error = V1Error(412, "Body is required")
        resp = make_response(jsonify(v1error), v1error.code)
        return resp, resp.status_code

    if connexion.request.mimetype == 'application/x-yml':
        
        # Check for the file already exists or not
        file_path = os.path.join(pvc_mount_path, file_name)
        if not os.path.exists(file_path):
            v1error = V1Error(400, "Threshold alarm rule file not found")
            resp = make_response(jsonify(v1error), v1error.code)
            return resp, resp.status_code
         
        try:
            # Decode the binary data to a string
            yaml_content_str = body.decode('utf-8')
            yaml_content = yaml.safe_load(yaml_content_str)
        except yaml.YAMLError as exc:
            ex_type, ex_val, tb = sys.exc_info()
            logger.error(f"exception cause in update status:{ex_type} and {ex_val}")
            traceback.print_tb(tb)
            v1error = V1Error(400, "Invalid YAML content")
            resp = make_response(jsonify(v1error), v1error.code)
            return resp, resp.status_code
        
    try:
        # Convert the parsed dictionary to the model
        v1_alarm_rule = V1alarmRule.from_dict(yaml_content)
        
        # Manual validation for required fields
        file_validation(v1_alarm_rule)
        
    except ValueError as exc:
        logger.error(f"exception cause in due to yaml validation of file {exc}")
        v1error = V1Error(400, f"Content not provided in proper format {exc}")
        resp = make_response(jsonify(v1error), v1error.code)
        return resp, resp.status_code
    
     # Save the file to the PVC (Assuming the PVC is mounted at /mnt/pvc)
    file_path = os.path.join(pvc_mount_path, file_name)
    with open(file_path, 'w') as f:
        f.write(yaml_content_str)

    resp = make_response()
    resp.content_type = 'application/json'
    resp.data = json.dumps({"code": 201, "message": "File updated successfully"})
    return resp, 201


def delete_rule_file(file_name):  # noqa: E501
    """Delete threshold alarms rule file

    This API is used to delete the threshold alarms rule file provided. # noqa: E501

    :param file_name:
    :type file_name: str

    :rtype: None
    """
    
    file_path = os.path.join(pvc_mount_path, file_name)

    if not os.path.exists(file_path):
        v1error = V1Error(404, "Threshold alarms rule file not found")
        return jsonify(v1error), 404

    try:
        os.remove(file_path)
        return make_response(jsonify({"code": 200, "message": "File deleted successfully"}), 200)
    except Exception as e:
        v1error = V1Error(500, f"An unexpected error occurred: {str(e)}")
        return jsonify(v1error), 500
    
def file_validation(v1_alarm_rule):
    if v1_alarm_rule.groups:
            for group in v1_alarm_rule.groups:
            
                if not getattr(group, 'name', None):
                    raise ValueError("'name' field is required and cannot be empty")
                
                if not getattr(group, 'rules', None):
                    raise ValueError("'rules' field is required and cannot be empty")
                
                for rule in group.rules:
                    if not rule.get('alert', None) and not rule.get('record', None):
                        raise ValueError("Each rule must have either 'alert' or 'record'")

                    if not rule.get('expr', None):
                        raise ValueError("Rule 'expr' is required when 'alert' is provided and cannot be empty")                    
    else:
        raise ValueError("'groups' field is required")