import json
import logging

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError, NotFoundError 

class OpenSearchDB(object):
    
    def __init__(self):
        self.logger = logging.getLogger("WeatherApp")
        self.es = Elasticsearch("localhost:9200", timeout=30, max_retries=3, 
                                retry_on_timeout=True)
    
    def read_doc(self, index_name, doc_id):
        try:
            self.logger.info(f"Reading {doc_id} from {index_name}")
            doc = self.es.get(index=index_name, id=doc_id)
            return doc
        except NotFoundError as ex:
            self.logger.error(f"Exception occurred during read operation on 
                              Opensearch with {ex}")
            return None
    
    def delete_doc(self, index_name, doc_id):
        self.logger.info(f"Deletion of id: {doc_id} from index: {index_name}")
        result = self.es.delete(index=index_name, id=doc_id)
        return result
    
    def create_doc(self, index_name, body, doc_id=None):
        self.logger.info(f"Pushing Data : {body} to {index_name}")
        if doc_id is None:
            result = self.es.index(index=index_name, body=json.dumps(body))
        else:
            result = self.es.create(index=index_name, id=doc_id, body=json.dumps(body))
        return result
    
    def update_doc(self, index_name, body):
        pass
    
    def create_index(self, index_name):
        pass