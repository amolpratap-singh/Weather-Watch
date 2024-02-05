import logging

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError, NotFoundError 

class OpenSearchDB(object):
    
    def __init__(self):
        self.logger = logging.getLogger("WeatherApp")
        self.es = Elasticsearch("localhost:9200", timeout=30, max_retries=3, 
                                retry_on_timeout=True)
    
    def read_doc(self, index_name, doc_id):
        pass
    
    def delete_doc(self, index_name, doc_id):
        pass
    
    def update_doc(self, index_name, body):
        pass
    
    def create_doc(self, index_name, body, key=None):
        pass