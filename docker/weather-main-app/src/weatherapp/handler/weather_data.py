import logging
from threading import Thread

from weatherapp.handler.geo_location import GeoLocation

class WeatherData(Thread):
    
    def __init__(self, thread_name, thread_id):
        Thread.__init__(self)
        self.logger = logging.getLogger("WeatherApp")
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.geo_loc = GeoLocation()
        self.pincode_list = self.geo_loc.get_pincode_list()
    
    def _run(self):
        self.logger.info(f"Weather thread started {self.thread_id} and {self.thread_name}")