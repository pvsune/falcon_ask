import pytest
from datetime import datetime

from falcon_ask import FalconAskMiddleware


@pytest.fixture()
def body():
    return {
        'request': {
            'type': 'LaunchRequest'
        }
    }


@pytest.fixture()
def middleware():
    return FalconAskMiddleware(None)


def test_validate_request_timestamp(body, middleware):
    res = middleware.validate_request_timestamp(body)
    assert res is False

    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    body['request']['timestamp'] = now
    res = middleware.validate_request_timestamp(body)
    assert res
