import os
import json
import logging

from weatherapp.handler import constant
from weatherapp.opensearchdb.opensearchdb import OpenSearchDB

COUNTRY_CODE="IN"

current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_dir, "..", "resources", "test-pincodes.json")
absolute_path = os.path.abspath(relative_path)



class GeoLocation(object):
    
    def __init__(self):
        self.logger = logging.getLogger("WeatherApp")
        self.file_path = absolute_path
        self.opensearchdb = OpenSearchDB()
    
    def read_input_file(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            self.logger.error(f"File is not present at {self.file_path}")
            return None
        except json.JSONDecodeError:
            self.logger.error(f"Error caused during decoding json {self.file_path} file")
            
    def update_geolocation(self):
        
        json_data = self.read_input_file()
        if json_data:
            for data in json_data:
                location_info = dict()
                key = str(data.get(constant.PINCODE)) + "_" + COUNTRY_CODE
                location_info[constant.PINCODE] = data.get(constant.PINCODE)
                location_info[constant.TALUKA] = data.get("taluk")
                location_info[constant.DISTRICT] = data.get("districtName")
                location_info[constant.STATE] = data.get("stateName")
                location_info[constant.COUNTRY_CODE] = COUNTRY_CODE
                location_info[constant.POST_OFFICE] = data.get("officeName")
                
                if self.opensearchdb.read_doc(index_name="geo-location", doc_id=key) is None:
                    self.logger.info(f"Geo location push in index geo-location with key: {key} and body:{location_info}")
                    self.opensearchdb.create_doc(index_name="geo-location", body=location_info, doc_id=key)
                else:
                    self.logger.info("key is already present in geo-location index")
            return True
        return False
    
    
    def get_pincode_list(self):
        pincode_list = list()
        data = self.opensearchdb.get_all_doc(index_name="geo-location")
        if data is not None:
            for var in data:
                pincode_list.append(var.get("pincode"))
        self.logger.info(f"List of Pincode present for geo-location: {pincode_list}")
        return pincode_list
        