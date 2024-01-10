import json
from unittest.mock import patch
import os


@patch.dict(os.environ, {"DISABLE_XRAY": "True"})
def test_ping_pong():
    # Arrange
    from functions.Ping.app import lambda_handler

    # Act
    response = lambda_handler({}, {})

    # Assert the response
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body["message"] == "Pong"
