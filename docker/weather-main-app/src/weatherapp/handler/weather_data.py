import time
import urllib3
import logging
import requests
import schedule

from datetime import datetime
from threading import Thread

from weatherapp.handler import constant
from weatherapp.utils.retry import retry_on_exception
from weatherapp.handler.geo_location import GeoLocation
from weatherapp.opensearchdb.opensearchclient import OpenSearchDB

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WeatherData(Thread):
    
    def __init__(self, thread_name, thread_id):
        Thread.__init__(self)
        self.logger = logging.getLogger("WeatherApp")
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.host_weather_url = constant.HOST_WEATHER_URL
        self.api_key = constant.API_KEY
        self.history_index_name = "history-weather" + "." + datetime.today().strftime("%Y-%m-%d-%H")
        self.opensearchdb = OpenSearchDB()
        self.geo_loc = GeoLocation()
        self.pincode_list = self.geo_loc.get_pincode_list()
    
    def run(self):
        self.logger.info(f"Weather thread started {self.thread_id} and {self.thread_name}")
        for pincode in range(len(self.pincode_list)):
            self._set_weather_data(self.pincode_list[pincode])
        #self.logger.info("Jobs been trigger for every 600 seconds")
        #schedule.every(6).hours.do(self.jobs())
        #schedule.every(600).seconds.do(self.jobs)
        #while True:
        #    schedule.run_pending()
        #    time.sleep(1)
    
    #def jobs(self):
    #    self.logger.info("Jobs been schedule for every 600 seconds")
    #    for pincode in range(len(self.pincode_list)):
    #        self._set_weather_data(self.pincode_list[pincode])
    
    @retry_on_exception(Exception, wait_time=1, delay=2)
    def _set_weather_data(self, pincode):
        read_key = str(str(pincode) + "_" + constant.COUNTRY_CODE)
        location_data = self.opensearchdb.read_doc(index_name="geo-location", doc_id=read_key)
        params = {
            "lat": location_data.get("lat"),
            "lon": location_data.get("lon"),
            "units": "metric",
            "lang": "en",
            "appid": self.api_key
        }
        
        key = str(pincode) + "_" + location_data.get(constant.DISTRICT).replace(" ","") \
        + "_" + location_data.get(constant.STATE).replace(" ","") + "_" + constant.COUNTRY_CODE
        
        try:
            if location_data.get("lat") and location_data.get("lon"):
                self.logger.info("Current Weather Requests been sent towards API")
                response = requests.get(self.host_weather_url, params, verify=False)
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
            self.logger.error(f"http error while connecting {self.host_weather_url} with err: {http_err}")
            raise http_err(f"http error while connecting {self.host_weather_url} with err: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Error while connecting {self.host_weather_url} with err: {conn_err}")
            raise conn_err(f"Error while connecting {self.host_weather_url} with err: {conn_err}")
        except requests.exceptions.Timeout as time_out_err:
            self.logger.error(f"Time out error occur while connecting {self.host_weather_url} with err: {time_out_err}")
            raise time_out_err(f"Time out error occur while connecting {self.host_weather_url} with err: {time_out_err}")
        except Exception as ex:
            self.logger.error(f"Error occured while connecting {self.host_weather_url} with {ex}")
            raise ex(f"Error occured while connecting {self.host_weather_url} with {ex}")
    
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