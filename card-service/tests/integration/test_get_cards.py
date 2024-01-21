import json
import os
from unittest.mock import patch
from .conftest import DYNAMODB_TABLE_NAME


@patch.dict(os.environ, {"DYNAMODB_TABLE_NAME": DYNAMODB_TABLE_NAME, "DISABLE_XRAY": "True"})
def test_get_collection(setup_dynamodb):
    from functions.get_cards.app import lambda_handler

    # Insert mock data into the table
    table = setup_dynamodb
    table.put_item(Item={'PK': 'OracleId#517be4da-9aa0-4a83-a559-962df0450f2c', 'SK': 'PrintId#faf65512-8228-48f4-ba7b-d861b66d28c9#Card', "GSI1PK": 'PrintId#faf65512-8228-48f4-ba7b-d861b66d28c9', 'GSI1SK': 'Card', 'DataType': 'Card'})
    table.put_item(Item={'PK': 'OracleId#517be4da-9aa0-4a83-a559-962df0450f2c', 'SK': 'PrintId#faf65512-8228-48f4-ba7b-d861b66d28c9#Face#1', "GSI1PK": 'PrintId#faf65512-8228-48f4-ba7b-d861b66d28c9', 'GSI1SK': 'Face#1', 'DataType': 'Face'})

    # Mock API Gateway event
    event = {'queryStringParameters': {'oracle_id': '517be4da-9aa0-4a83-a559-962df0450f2c'}}

    # Invoke the lambda handler
    response = lambda_handler(event, {})

    # Assert the response
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert len(body) == 2
