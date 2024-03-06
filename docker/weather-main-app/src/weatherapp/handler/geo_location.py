import os
import json
import logging
import requests

from src.weatherapp.handler import constant
from src.weatherapp.utils.retry import retry_on_exception
from src.weatherapp.Exception.exceptions import EmptyListError
from src.weatherapp.opensearchdb.opensearchclient import OpenSearchDB

current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_dir, "..", "resources", "pincodes.json")
absolute_path = os.path.abspath(relative_path)

class GeoLocation(object):
    
    def __init__(self):
        self.logger = logging.getLogger("WeatherApp")
        self.file_path = absolute_path
        self.opensearchdb = OpenSearchDB()
        self.host_url = constant.HOST_URL
        self.api_key = constant.API_KEY
    
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
                key = str(data.get(constant.PINCODE)) + "_" + constant.COUNTRY_CODE
                location_info[constant.PINCODE] = data.get(constant.PINCODE)
                location_info[constant.TALUKA] = data.get("taluk")
                location_info[constant.DISTRICT] = data.get("districtName")
                location_info[constant.STATE] = data.get("stateName")
                location_info[constant.COUNTRY_CODE_KEY] = constant.COUNTRY_CODE
                location_info[constant.POST_OFFICE] = data.get("officeName")
                
                if self.opensearchdb.read_doc(index_name="geo-location", doc_id=key) is None:
                    self.logger.info(f"Geo location push in index geo-location with key: {key} and body:{location_info}")
                    self.opensearchdb.create_doc(index_name="geo-location", body=location_info, doc_id=key)
                else:
                    self.logger.info("key is already present in geo-location index")
            return True
        return False
    
    @retry_on_exception(Exception, wait_time=10, max_retry=5, delay=5)
    def get_pincode_list(self):
        pincode_list = list()
        data = self.opensearchdb.get_all_doc(index_name="geo-location")
        if data is not None:
            for var in data:
                pincode_list.append(var.get("pincode"))
        try:
            if not pincode_list:
                raise ValueError(f"pincode list is empty {len(pincode_list)}")
        except EmptyListError as ex:
            self.logger.error(f"pincode list is empty {ex}")
        self.logger.info(f"List of Pincode present for geo-location: {pincode_list}")
        return pincode_list
    
    def update_lat_lon_db(self):
        pincode_list = self.get_pincode_list()
        for pincode in range(len(pincode_list)):
            key = str(str(pincode_list[pincode]) + "_" + constant.COUNTRY_CODE)
            result = self.opensearchdb.read_doc(index_name="geo-location", doc_id=key)
            if constant.LATITUDE not in result.keys() and constant.LONGITUDE not in result.keys():
                self._set_lat_lon_db(pincode_list[pincode])
    
    @retry_on_exception(Exception, wait_time=1, delay=2)
    def _set_lat_lon_db(self, pincode):
        params = {
            "zip": f"{pincode},IN",
            "appid": self.api_key
        }
        
        try:
            response = requests.get(self.host_url, params, verify=False)
        
            if response.status_code == 200:
                key = str(str(pincode) + "_" + constant.COUNTRY_CODE)
                body = {
                    "lat": response.json().get("lat", ""),
                    "lon": response.json().get("lon", "")
                }
                self.opensearchdb.update_doc(index_name="geo-location",doc_id=key,body=body)
            else:
                self.logger.info(f"Receive status code as {response.status_code}")
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"http error while connecting {self.host_url} with err: {http_err}")
            raise http_err(f"http error while connecting {self.host_url} with err: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Error while connecting {self.host_url} with err: {conn_err}")
            raise conn_err(f"Error while connecting {self.host_url} with err: {conn_err}")
        except requests.exceptions.Timeout as time_out_err:
            self.logger.error(f"Time out error occur while connecting {self.host_url} with err: {time_out_err}")
            raise time_out_err(f"Time out error occur while connecting {self.host_url} with err: {time_out_err}")
        except Exception as ex:
            self.logger.error(f"Error occured while connecting {self.host_url} with {ex}")
            raise ex(f"Error occured while connecting {self.host_url} with {ex}")
        