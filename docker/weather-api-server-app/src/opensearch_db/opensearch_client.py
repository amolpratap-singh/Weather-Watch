import os
import json
import logging
import urllib3

from opensearchpy import OpenSearch
from opensearchpy.exceptions import NotFoundError

#OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST","localhost")
#OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT",9200))

OPENSEARCH_HOST = "localhost"
OPENSEARCH_PORT = 9200

#AUTH = ('admin', 'admin')
AUTH = ('admin', 'weatherTest@123')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO Enable cert or TLS as well
def get_opensearch_client():
    es = OpenSearch(hosts=[{"hosts": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
                             http_auth=AUTH, use_ssl=True, verify_certs=False, 
                             ssl_assert_hostname = False, ssl_show_warn = False)
    
    return es
    
def close_opensearch_client(es_client):
    es_client.close()
    