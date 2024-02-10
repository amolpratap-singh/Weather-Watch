
import logging

from threading import Thread

class AirQualityIndex(Thread):
    
    def __init__(self, thread_name, thread_id):
        Thread.__init__(self)
        self.logger = logging.getLogger("WeatherApp")
        self.thread_name = thread_name
        self.thread_id = thread_id
    
    def run(self):
        self.logger.info(f"Air Quality index thread started {self.thread_id} and {self.thread_name}")