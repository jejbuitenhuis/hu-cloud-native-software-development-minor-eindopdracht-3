import os
import json
import logging
from unittest.mock import patch
from .jwt_generator import generate_test_jwt
from .conftest import DYNAMODB_TABLE_NAME

COGINTO_USERNAME = "test@example.com"
COGINTO_PASSWORD = "NewPassword456!"

logger = logging.getLogger()
logger.setLevel("INFO")


@patch.dict(
    os.environ,
    {
        "DYNAMODB_TABLE": DYNAMODB_TABLE_NAME,
        "DISABLE_XRAY": "True",
        "EVENT_BUS_ARN": "",
    },
)
def test_search_oraclename(setup_dynamodb_collection_with_items):
    from functions.Search.app import lambda_handler

    event = {
        "headers": {"Authorization": f"Bearer {generate_test_jwt()}"},
        "queryStringParameters": {"q": "Beloved"},
    }

    # Act
    result = lambda_handler(event, None)

    body = json.loads(result["body"])

    # Assert
    assert body["Items"][0]["PK"] == "USER#test-user"
    assert body["Items"][0]["SK"] == "CardInstance#1"
    assert body["Items"][0]["OracleName"] == "Beloved Beggar // Generous Soul"


@patch.dict(
    os.environ,
    {
        "DYNAMODB_TABLE": DYNAMODB_TABLE_NAME,
        "DISABLE_XRAY": "True",
        "EVENT_BUS_ARN": "",
    },
)
def test_search_oracletext(setup_dynamodb_collection_with_items):
    from functions.Search.app import lambda_handler

    event = {
        "headers": {"Authorization": f"Bearer {generate_test_jwt()}"},
        "queryStringParameters": {"q": "Graveyard"},
    }

    # Act
    result = lambda_handler(event, None)

    body = json.loads(result["body"])

    # Assert
    assert body["Items"][0]["PK"] == "USER#test-user"
    assert body["Items"][0]["SK"] == "CardInstance#1"
    assert body["Items"][0]["OracleName"] == "Beloved Beggar // Generous Soul"


@patch.dict(
    os.environ,
    {
        "DYNAMODB_TABLE": DYNAMODB_TABLE_NAME,
        "DISABLE_XRAY": "True",
        "EVENT_BUS_ARN": "",
    },
)
def test_search_not_found(setup_dynamodb_collection):
    from functions.Search.app import lambda_handler

    # Arrange
    event = {
        "headers": {"Authorization": f"Bearer {generate_test_jwt()}"},
        "queryStringParameters": {"q": "Invalid"},
    }

    # Act
    result = lambda_handler(event, None)

    # Assert
    assert result["statusCode"] == 404


@patch.dict(
    os.environ,
    {
        "DYNAMODB_TABLE": DYNAMODB_TABLE_NAME,
        "DISABLE_XRAY": "True",
        "EVENT_BUS_ARN": "",
    },
)
def test_search_no_authorization(setup_dynamodb_collection):
    from functions.Search.app import lambda_handler

    # Arrange
    event = {
        "queryStringParameters": {"q": "Invalid"},
    }

    # Act
    result = lambda_handler(event, None)
    body = json.loads(result["body"])

    # Assert
    assert result["statusCode"] == 401
    assert body["Message"] == "JWT token not provided"


def test_search_no_query(setup_dynamodb_collection):
    from functions.Search.app import lambda_handler

    # Arrange
    event = {
        "headers": {"Authorization": generate_test_jwt()},
    }

    # Act
    result = lambda_handler(event, None)
    body = json.loads(result["body"])

    # Assert
    assert result["statusCode"] == 406
    assert body["Message"] == "query string parameter not provided"
