import os
from unittest.mock import patch
from moto import mock_dynamodb

COGINTO_USERNAME = "test@example.com"
COGINTO_PASSWORD = "NewPassword456!"


@patch.dict(os.environ, {"DISABLE_XRAY": "True", "EVENT_BUS_ARN": ""})
def test_search_works(setup_dynamodb_deck_with_item):
    from functions.Search.app import lambda_handler

    event = {
        "headers": {"token": "valid_id_token"},
        "queryStringParameters": {"q": "doctor"},
    }

    # Act
    result = lambda_handler(event, None)

    # Assert
    expected_output = {"statuscode": 200, "body": '{"item": "result"}'}

    assert result == expected_output


@patch.dict(os.environ, {"DISABLE_XRAY": "True", "EVENT_BUS_ARN": ""})
def test_search_not_found(setup_dynamodb_deck):
    from functions.Search.app import lambda_handler

    # Arrange

    event = {
        "headers": {"token": "valid_id_token"},
        "queryStringParameters": {"q": "invalid"},
    }

    # Act
    result = lambda_handler(event, None)

    # Assert
    expected_output = {
        "statuscode": 404,
        "body": "",
    }

    assert result == expected_output
