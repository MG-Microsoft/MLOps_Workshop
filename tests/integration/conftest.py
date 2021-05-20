import pytest

def pytest_addoption(parser):
    parser.addoption("--scoreurl", action="store",
        help="the score url of the ml web service")
    parser.addoption("--scorekey", action="store",
        help="the score key of the ml web service")

@pytest.fixture
def scoreurl(request):
    return request.config.getoption("--scoreurl")

@pytest.fixture
def scorekey(request):
    return request.config.getoption("--scorekey")
