import json
import os
from unittest.mock import patch
from .jwt_generator import generate_test_jwt


@patch.dict(os.environ, {"DYNAMODB_TABLE": "test-table", "DISABLE_XRAY": "True"})
def test_get_collection(setup_dynamodb_collection):
    from functions.get_collection.app import lambda_handler

    # Insert mock data into the table
    table = setup_dynamodb_collection
    table.put_item(Item={'PK': 'USER#test-user', 'SK': 'CardInstanceId#1#Card', 'CardInstanceId': '1', 'DataType': 'Card', 'DeckId': '1', 'GSI1SK': 'DeckId#1'})
    table.put_item(Item={'PK': 'USER#test-user', 'SK': 'CardInstanceId#2#Card', 'CardInstanceId': '2', 'DataType': 'Card'})

    # Mock API Gateway event
    event = {'headers': {'Authorization': f'Bearer {generate_test_jwt()}'}}

    # Invoke the lambda handler
    response = lambda_handler(event, {})

    # Assert the response
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert len(body) == 2
