import logging

from threading import Thread

class ForeCastNews(Thread):
    
    def __init__(self, thread_name, thread_id):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.logger = logging.getLogger("WeatherApp")
        
    def run(self):
        self.logger.info(f"Forecast news thread started {self.thread_id} and {self.thread_name}")