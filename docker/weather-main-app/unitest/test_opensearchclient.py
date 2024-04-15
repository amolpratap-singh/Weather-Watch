import pytest
from unittest.mock import MagicMock, patch
from opensearchpy.exceptions import NotFoundError
from src.weatherapp.opensearchdb.opensearchclient import OpenSearchDB

@pytest.fixture
def mocked_opensearch():
    return OpenSearchDB()

def test_read_doc_successful(mocked_opensearch, caplog):
    with patch.object(mocked_opensearch.es, 'get', return_value={"_source": {"key": "value"}}):
        doc = mocked_opensearch.read_doc("index_name", "doc_id")
        assert doc == {"key": "value"}
        assert "Reading doc_id from index_name" in caplog.text

def test_read_doc_not_found(mocked_opensearch, caplog):
    with patch.object(mocked_opensearch.es, 'get', side_effect=NotFoundError):
        doc = mocked_opensearch.read_doc("index_name", "doc_id")
        assert doc is None
        assert "Exception occurred during read operation on Opensearch" in caplog.text

def test_delete_doc(mocked_opensearch, caplog):
    with patch.object(mocked_opensearch.es, 'delete', return_value={"result": "deleted"}):
        result = mocked_opensearch.delete_doc("index_name", "doc_id")
        assert result == {"result": "deleted"}
        assert "Deletion of id: doc_id from index: index_name" in caplog.text

def test_create_doc(mocked_opensearch, caplog):
    with patch.object(mocked_opensearch.es.indices, 'create', return_value={"result": "created"}):
        result = mocked_opensearch.create_doc("index_name", {"key": "value"})
        assert result == {"result": "created"}
        assert "Pushing Data : {'key': 'value'} to index_name" in caplog.text

def test_update_doc(mocked_opensearch, caplog):
    with patch.object(mocked_opensearch.es, 'update'):
        mocked_opensearch.update_doc("index_name", "doc_id", {"key": "value"})
        assert "Update request sent to search body for: {'key': 'value'}" in caplog.text

def test_create_index(mocked_opensearch, caplog):
    with patch.object(mocked_opensearch.es.indices, 'create', return_value={"result": "created"}):
        mocked_opensearch.create_index("index_name", {"key": "value"})
        assert "Index creation request sent to search body for: {'key': 'value'}" in caplog.text

def test_get_all_doc_successful(mocked_opensearch, caplog):
    hits = [{'_source': {'key': 'value'}}]
    with patch.object(mocked_opensearch.es, 'search', return_value={'hits': {'hits': hits}}):
        documents = mocked_opensearch.get_all_doc("index_name")
        assert documents == [{"key": "value"}]
        assert "Exception occurred during getting pincode list" not in caplog.text

def test_get_all_doc_not_found(mocked_opensearch, caplog):
    with patch.object(mocked_opensearch.es, 'search', side_effect=NotFoundError):
        documents = mocked_opensearch.get_all_doc("index_name")
        assert documents is None
        assert "Exception occurred during getting pincode list" in caplog.text
