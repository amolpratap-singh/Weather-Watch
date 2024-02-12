import logging
import requests

from threading import Thread

from weatherapp.handler import constant
from weatherapp.handler.geo_location import GeoLocation
from weatherapp.opensearchdb.opensearchclient import OpenSearchDB

class WeatherData(Thread):
    
    def __init__(self, thread_name, thread_id):
        Thread.__init__(self)
        self.logger = logging.getLogger("WeatherApp")
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.opensearchdb = OpenSearchDB()
        self.geo_loc = GeoLocation()
        self.pincode_list = self.geo_loc.get_pincode_list()
    
    def run(self):
        self.logger.info(f"Weather thread started {self.thread_id} and {self.thread_name}")
        self.update_lat_long()
        
    def update_lat_long(self):
        url = "http://api.openweathermap.org/geo/1.0/zip"
        api_key = ""
        
        params = {
            "zip": f"{self.pincode_list[0]},IN",
            "appid": api_key
        }
        
        try:
            response = requests.get(url, params, verify=False)
        
            if response.status_code == 200:
                print(type(response.json()))
                print(response.json().get('lat'))
                print(response.json().get('lon'))
                key = str(str(self.pincode_list[0]) + "_" + constant.COUNTRY_CODE)
                body = {
                    "lat": response.json().get("lat"),
                    "lon": response.json().get("lon")
                }
                #self.opensearchdb.update_doc(index_name="geo-location",doc_id=key,body=body)
            else:
                self.logger.info(f"Receive status code as {response.status_code}")
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"http error while connecting {url}")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Error while connecting {url}")
        except requests.exceptions.Timeout as time_out_err:
            self.logger.error(f"Time out error occur while connecting {url}")
        except Exception as ex:
            self.logger.error(f"Error occured while connecting {url} with {ex}")