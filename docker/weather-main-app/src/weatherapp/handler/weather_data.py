import time
import logging
import requests

from datetime import datetime
from threading import Thread

from weatherapp.handler import constant
from weatherapp.handler.geo_location import GeoLocation
from weatherapp.opensearchdb.opensearchclient import OpenSearchDB

HOST_URL = "http://api.openweathermap.org/geo/1.0/zip"
HOST_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = ""

class WeatherData(Thread):
    
    def __init__(self, thread_name, thread_id):
        Thread.__init__(self)
        self.logger = logging.getLogger("WeatherApp")
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.history_index_name = "history-weather" + "." + datetime.today().strftime("%Y-%m-%d")
        self.opensearchdb = OpenSearchDB()
        self.geo_loc = GeoLocation()
        self.pincode_list = self.geo_loc.get_pincode_list()
    
    def run(self):
        self.logger.info(f"Weather thread started {self.thread_id} and {self.thread_name}")
        for pincode in range(len(self.pincode_list)):
            key = str(str(self.pincode_list[pincode]) + "_" + constant.COUNTRY_CODE)
            result = self.opensearchdb.read_doc(index_name="geo-location", doc_id=key)
            if constant.LATITUDE not in result.keys() and constant.LONGITUDE not in result.keys():
                self._set_lat_lon_db(self.pincode_list[pincode])
        
        for pincode in range(len(self.pincode_list)):
            self._set_weather_data(self.pincode_list[pincode])
    
    def _set_lat_lon_db(self, pincode):
        params = {
            "zip": f"{pincode},IN",
            "appid": API_KEY
        }
        
        try:
            response = requests.get(HOST_URL, params, verify=False)
        
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
            self.logger.error(f"http error while connecting {HOST_URL} with err: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Error while connecting {HOST_URL} with err: {conn_err}")
        except requests.exceptions.Timeout as time_out_err:
            self.logger.error(f"Time out error occur while connecting {HOST_URL} with err: {time_out_err}")
        except Exception as ex:
            self.logger.error(f"Error occured while connecting {HOST_URL} with {ex}")
    
    def _set_weather_data(self, pincode):
        read_key = str(str(pincode) + "_" + constant.COUNTRY_CODE)
        location_data = self.opensearchdb.read_doc(index_name="geo-location", doc_id=read_key)
        params = {
            "lat": location_data.get("lat"),
            "lon": location_data.get("lon"),
            "units": "metric",
            "lang": "en",
            "appid": API_KEY
        }
        
        key = str(pincode) + "_" + location_data.get(constant.DISTRICT) \
        + "_" + location_data.get(constant.DISTRICT) + "_" + constant.COUNTRY_CODE
        
        try:
            if location_data.get("lat") and location_data.get("lon"):
                response = requests.get(HOST_WEATHER_URL, params, verify=False)
                if response.status_code == 200:
                    if self.opensearchdb.read_doc(index_name="current-weather", doc_id=key) is None:
                        self.opensearchdb.create_doc(index_name="current-weather", doc_id=key,
                                                     body=self._set_body_data(location_data, response))
                    else:
                        self.opensearchdb.update_doc(index_name="current-weather", doc_id=key,
                                                     body=self._set_body_data(location_data, response))
                    if self.opensearchdb.read_doc(index_name=self.history_index_name, doc_id=key) is None:
                        self.logger.info(f"Weather data is not present in the history data for index:{self.history_index_name}")
                        self.opensearchdb.create_doc(index_name=self.history_index_name, doc_id=key,
                                                     body=self._set_body_data(location_data, response))
                else:
                    self.logger.info(f"Receive status code as {response.status_code}")
            else:
                self.logger.info(f"{pincode} doesn't contain latitude and longitude skipping the task")
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"http error while connecting {HOST_URL} with err: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Error while connecting {HOST_URL} with err: {conn_err}")
        except requests.exceptions.Timeout as time_out_err:
            self.logger.error(f"Time out error occur while connecting {HOST_URL} with err: {time_out_err}")
        except Exception as ex:
            self.logger.error(f"Error occured while connecting {HOST_URL} with {ex}")
    
    def _set_body_data(self, location_data, response):
        body = dict()
        body[constant.LOCATION] = location_data
        body[constant.WIND] = response.json().get("wind", "")
        body[constant.WEATHER] = response.json().get("main", "")
        weather_info = response.json().get("weather", None)
        if weather_info is not None:
            body[constant.WEATHER_CODE] = weather_info[0].get("id", "")
            body[constant.DESCRIPTION] = weather_info[0].get("description", "")
        body[constant.EPOCH_TIME] = int(time.time())
        body[constant.SOURCE_DATE] = response.json().get("dt", "")
        body[constant.SOURCE_TIME_ZONE] = response.json().get("timezone", "")
        body[constant.EVENT_TIME] = self._get_event_time()
        return body
    
    def _get_event_time(self):
        current_time = datetime.now()
        return current_time.strftime("%d-%m-%y %H:%M:%S")