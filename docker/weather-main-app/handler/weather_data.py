
<<<<<<< HEAD
=======
import json
>>>>>>> 3f23598 (Opensearch DB docker and Client Api Implementation)
import logging

from threading import Thread

class WeatherData(Thread):
    
    def __init__(self, thread_name, thread_id):
        Thread.__init__(self)
        self.logger = logging.getLogger("WeatherApp")
        self.thread_name = thread_name
        self.thread_id = thread_id
<<<<<<< HEAD
    
    def run(self):
        self.logger.info(f"Weather thread started {self.thread_id} and {self.thread_name}")
=======
        #self.pincode_list = list()
    
    def _run(self):
        self.logger.info(f"Weather thread started {self.thread_id} and {self.thread_name}")
        
    # TODO South Bound design in POC phase    
    def get_pincodes(self):
        pass
>>>>>>> 3f23598 (Opensearch DB docker and Client Api Implementation)
