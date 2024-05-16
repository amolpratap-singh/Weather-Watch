import os
import json
import logging
import urllib3

from opensearchpy import OpenSearch
from opensearchpy.exceptions import NotFoundError

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST","localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT",9200))

AUTH = ('admin', 'weatherTest@123')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OpenSearchDB(object):
    
    def __init__(self):
        self.logger = logging.getLogger("WeatherApp")
        self.es = OpenSearch(hosts=[{"hosts": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
                             http_auth=AUTH, use_ssl=True, verify_certs=False, 
                             ssl_assert_hostname = False, ssl_show_warn = False)
    
    def read_doc(self, index_name, doc_id):
        try:
            self.logger.info(f"Reading {doc_id} from {index_name}")
            doc = self.es.get(index=index_name, id=doc_id)
            return doc["_source"]
        except NotFoundError as ex:
            self.logger.error(f"Exception occurred during read operation on Opensearch with {ex}")
            return None
    
    def delete_doc(self, index_name, doc_id):
        self.logger.info(f"Deletion of id: {doc_id} from index: {index_name}")
        result = self.es.delete(index=index_name, id=doc_id)
        return result
    
    def create_doc(self, index_name, body, doc_id=None):
        self.logger.info(f"Pushing Data : {body} to {index_name}")
        if doc_id is None:
            result = self.es.indices.create(index=index_name, body=json.dumps(body))
        else:
            result = self.es.index(index=index_name, id=doc_id, body=json.dumps(body))
        return result
    
    def update_doc(self, index_name, doc_id, body):
        self.logger.info(f"Update request sent to search body for: {body}")
        self.es.update(index=index_name, id=doc_id, body={"doc": body})
    
    def create_index(self, index_name, body):
        self.es.indices.create(index=index_name, body=json.dumps(body))
        
    def get_all_doc(self, index_name):
        query = {
            "query": {"match_all": {}},
            "size": 1000
        }
        try:
            response = self.es.search(index=index_name, body=query)
            documents = [hit['_source'] for hit in response['hits']['hits']]
            return documents
        except NotFoundError as ex:
            self.logger.error(f"Exception occurred during getting pincode list {ex}")
            return None