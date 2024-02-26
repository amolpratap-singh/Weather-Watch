import time
import logging
import requests

from datetime import datetime
from threading import Thread

from weatherapp.handler import constant
from weatherapp.utils.retry import retry_on_exception
from weatherapp.utils.schedule_jobs import schedule_interval
from weatherapp.opensearchdb.opensearchclient import OpenSearchDB
from weatherapp.handler.geo_location import GeoLocation

class AirQualityIndex(Thread):
    
    def __init__(self, thread_name, thread_id):
        Thread.__init__(self)
        self.logger = logging.getLogger("WeatherApp")
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.host_aqi_url = constant.HOST_AQI_URL
        self.api_key = constant.API_KEY
        self.history_aqi_index_name = "history-aqi" + "." + datetime.today().strftime("%Y-%m-%d-%H")
        self.opensearchdb = OpenSearchDB()
        self.geo_loc = GeoLocation()
        self.pincode_list = self.geo_loc.get_pincode_list()
    
    def run(self):
        self.logger.info(f"AQI thread started {self.thread_id} and {self.thread_name}")
        self.logger.info(f"AQI Jobs been trigger for every {12} Hours")
        self._start()
    
    @schedule_interval(12)
    def _start(self):
        self.logger.info("Update of AQI Data in DB triggered")
        for pincode in range(len(self.pincode_list)):
            self._set_weather_data(self.pincode_list[pincode])
        
    @retry_on_exception(Exception, wait_time=1, delay=2)
    def _set_aqi_data(self, pincode):
        read_key = str(str(pincode) + "_" + constant.COUNTRY_CODE)
        location_data = self.opensearchdb.read_doc(index_name="geo-location", doc_id=read_key)
        params = {
            "lat": location_data.get("lat"),
            "lon": location_data.get("lon"),
            "appid": self.api_key
        }
        
        key = str(pincode) + "_" + location_data.get(constant.DISTRICT).replace(" ","") \
        + "_" + location_data.get(constant.STATE).replace(" ","") + "_" + constant.COUNTRY_CODE
        
        try:
            if location_data.get("lat") and location_data.get("lon"):
                self.logger.info("AQI Requests been sent towards API")
                response = requests.get(self.host_aqi_url, params, verify=False)
                if response.status_code == 200:
                    if self.opensearchdb.read_doc(index_name="current-aqi", doc_id=key) is None:
                        self.opensearchdb.create_doc(index_name="current-aqi", doc_id=key,
                                                     body=self._set_aqi_body_data(location_data, response))
                    else:
                        self.opensearchdb.update_doc(index_name="current-aqi", doc_id=key,
                                                     body=self._set_aqi_body_data(location_data, response))
                    if self.opensearchdb.read_doc(index_name=self.history_aqi_index_name, doc_id=key) is None:
                        self.logger.info(f"AQI data is not present in the history data for index:{self.history_aqi_index_name}")
                        self.opensearchdb.create_doc(index_name=self.history_aqi_index_name, doc_id=key,
                                                     body=self._set_aqi_body_data(location_data, response))
                else:
                    self.logger.info(f"Receive status code as {response.status_code} for AQI")
            else:
                self.logger.info(f"{pincode} doesn't contain latitude and longitude skipping the task")
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"http error while connecting {self.host_aqi_url} with err: {http_err}")
            raise http_err(f"http error while connecting {self.host_aqi_url} with err: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Error while connecting {self.host_aqi_url} with err: {conn_err}")
            raise conn_err(f"Error while connecting {self.host_aqi_url} with err: {conn_err}")
        except requests.exceptions.Timeout as time_out_err:
            self.logger.error(f"Time out error occur while connecting {self.host_aqi_url} with err: {time_out_err}")
            raise time_out_err(f"Time out error occur while connecting {self.host_aqi_url} with err: {time_out_err}")
        except Exception as ex:
            self.logger.error(f"Error occured while connecting {self.host_aqi_url} with {ex}")
            raise ex(f"Error occured while connecting {self.host_aqi_url} with {ex}")
    
    def _set_aqi_body_data(self, location_data, response):
        body = dict()
        body[constant.LOCATION] = location_data
        aqi_lists_data = response.json().get("list", None)
        if aqi_lists_data is not None:
            body[constant.AQI] = aqi_lists_data[0].get("main").get("aqi", None)
            body[constant.AQI_COMPONENTS] = aqi_lists_data[0].get("components", "")
            body[constant.SOURCE_DATE] = aqi_lists_data[0].get("dt", "")
        body[constant.EPOCH_TIME] = int(time.time())
        body[constant.EVENT_TIME] = self._get_event_time()
        return body
    
    def _get_event_time(self):
        current_time = datetime.now()
        return current_time.strftime("%d-%m-%y %H:%M:%S")