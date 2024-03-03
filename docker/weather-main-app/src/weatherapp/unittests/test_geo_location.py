import pytest

@pytest.fixture
def response():
    return 0 == 0

class TestGeoLocation(object):
    
    def setup_method(self, method):
        print(f"Setup method been called {method}")
        
    def teardown_method(self, method):
        print(f"Tear down method been called {method}")