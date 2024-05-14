import os
import urllib3
from opensearchpy import OpenSearch

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST","localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT",9200))

AUTH = ('admin', 'weatherTest@123')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_opensearch_client():
    es = OpenSearch([f"https://{OPENSEARCH_HOST}:{OPENSEARCH_PORT}"], http_auth=AUTH, verify_certs=False)
    return es
    
def close_opensearch_client(es_client):
    es_client.close()
    