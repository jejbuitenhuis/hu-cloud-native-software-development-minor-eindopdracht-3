import os
from unittest.mock import patch
from moto import mock_dynamodb
from .jwt_generator import generate_test_jwt

COGINTO_USERNAME = "test@example.com"
COGINTO_PASSWORD = "NewPassword456!"


@patch.dict(os.environ, {"DISABLE_XRAY": "True", "EVENT_BUS_ARN": ""})
def test_search_works(setup_dynamodb_collection_with_items):
    from functions.Search.app import lambda_handler

    event = {
        "headers": {"Authorization": generate_test_jwt()},
        "queryStringParameters": {"q": "doctor"},
    }

    # Act
    result = lambda_handler(event, None)

    # Assert
    expected_output = {
        "statuscode": 200,
        "body": {
            "Items": [
                {
                    "UserId": "123",
                    "UserName": "JohnDoe",
                    "Age": "30",
                    "Email": "john.doe@example.com",
                },
                {
                    "UserId": "456",
                    "UserName": "JaneSmith",
                    "Age": "25",
                    "Email": "jane.smith@example.com",
                },
            ],
        },
    }

    assert result == expected_output


@patch.dict(os.environ, {"DISABLE_XRAY": "True", "EVENT_BUS_ARN": ""})
def test_search_not_found(setup_dynamodb_collection):
    from functions.Search.app import lambda_handler

    # Arrange
    event = {
        "headers": {"Authorization": generate_test_jwt()},
        "queryStringParameters": {"q": "invalid"},
    }

    # Act
    result = lambda_handler(event, None)

    # Assert
    expected_output = {
        "statuscode": 404,
        "body": {"message": "Not found"},
        "headers": {
            "Content-Type": "application/json",
        },
    }

    assert result == expected_output
