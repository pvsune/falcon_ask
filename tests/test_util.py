import pytest

from falcon_ask.util import get_req_type


@pytest.fixture()
def body():
    return {
        'request': {
            'type': 'LaunchRequest'
        }
    }


def test_get_req_type(body):
    assert get_req_type(body) == 'LaunchRequest'
