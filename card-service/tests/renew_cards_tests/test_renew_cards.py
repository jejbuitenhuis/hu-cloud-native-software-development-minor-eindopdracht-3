import json
from unittest.mock import patch, MagicMock
import os
import pytest
import boto3
import requests
import requests_mock
from boto3.dynamodb.conditions import Key, Attr
from moto import mock_dynamodb

@pytest.fixture(scope="function")
@mock_dynamodb
def table():
    # Setup phase: Create table
    dynamodb = boto3.resource('dynamodb', 'us-east-1')
    table = dynamodb.create_table(
        TableName='test-card-table',
        KeySchema=[{'AttributeName': 'PK', 'KeyType': 'HASH'}, {'AttributeName': 'SK', 'KeyType': 'RANGE'}],
        AttributeDefinitions=[{"AttributeName": "PK", "AttributeType": "S"},
                              {"AttributeName": "SK", "AttributeType": "S"}],
        BillingMode='PAY_PER_REQUEST'
    )
    table.meta.client.get_waiter('table_exists').wait(TableName="test-card-table")

    # Provide the table to the test
    yield table

    # Teardown phase: Delete table
    # table.delete()

@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table"})
def test_renew_cards_writes_correct_data_single_face(requests_mock, table):
    with patch('boto3.client') as mock_client:
        os.environ["DYNAMODB_TABLE_NAME"] = "test-card-table"
        table.meta.client.get_waiter('table_exists').wait(TableName="test-card-table")

        mock_event_bridge = MagicMock()
        mock_client.return_value = mock_event_bridge

        bulk_data_mock_response = {
            "data": [
                {"type": "default_cards", "download_uri": "https://data.scryfall.io/default-cards/default-cards-20240116100428.json"}
            ]
        }
        with open('functions/renewEntities/single_face_card_list.json', 'r') as file:
            json_data = json.load(file)
        mock_file_content = json.dumps(json_data).encode('utf-8')

        requests_mock.get("https://api.scryfall.com/bulk-data", json=bulk_data_mock_response)
        requests_mock.get("https://data.scryfall.io/default-cards/default-cards-20240116100428.json", content=mock_file_content)

        # Invoke the lambda handler
        from functions.renewEntities.app import lambda_handler
        lambda_handler({}, {})

        single_face_card = table.query(
            KeyConditionExpression=Key('PK').eq('OracleId#44623693-51d6-49ad-8cd7-140505caf02f') & Key('SK').eq(
                'PrintId#0000579f-7b35-4ed3-b44c-db2a538066fe#Face#1')
        )

        assert requests_mock.called
        assert requests_mock.call_count == 2
        assert len(single_face_card['Items']) == 1
        assert single_face_card['Items'][0]['PK'] == "OracleId#44623693-51d6-49ad-8cd7-140505caf02f"
        assert single_face_card['Items'][0]['SK'] == "PrintId#0000579f-7b35-4ed3-b44c-db2a538066fe#Face#1"



@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table"})
def test_renew_cards_two_faced(requests_mock, table):
    with patch('boto3.client') as mock_client:
        os.environ["DYNAMODB_TABLE_NAME"] = "test-card-table"
        table.meta.client.get_waiter('table_exists').wait(TableName="test-card-table")

        mock_event_bridge = MagicMock()
        mock_client.return_value = mock_event_bridge

        bulk_data_mock_response = {
            "data": [
                {"type": "default_cards", "download_uri": "https://data.scryfall.io/default-cards/default-cards-20240116100428.json"}
            ]
        }
        with open('functions/renewEntities/double_faced_card_list.json', 'r') as file:
            json_data = json.load(file)
        mock_file_content = json.dumps(json_data).encode('utf-8')

        requests_mock.get("https://api.scryfall.com/bulk-data", json=bulk_data_mock_response)
        requests_mock.get("https://data.scryfall.io/default-cards/default-cards-20240116100428.json", content=mock_file_content)

        # Invoke the lambda handler
        from functions.renewEntities.app import lambda_handler
        lambda_handler({}, {})

        double_card_faces = table.query(
            KeyConditionExpression=Key('PK').eq('OracleId#562d71b9-1646-474e-9293-55da6947a758')
        )

        assert requests_mock.called
        assert requests_mock.call_count == 2
        assert len(double_card_faces['Items']) == 3
        for item in double_card_faces['Items']:
            assert item['PK'] == "OracleId#562d71b9-1646-474e-9293-55da6947a758"


@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table"})
def test_renew_cards_ten_cards(requests_mock, table):
    with patch('boto3.client') as mock_client:
        os.environ["DYNAMODB_TABLE_NAME"] = "test-card-table"
        dynamodb = boto3.resource('dynamodb', 'us-east-1')
        table = dynamodb.create_table(
            TableName='test-card-table',
            KeySchema=[{'AttributeName': 'PK', 'KeyType': 'HASH'}, {'AttributeName': 'SK', 'KeyType': 'RANGE'}],
            AttributeDefinitions=[{"AttributeName": "PK", "AttributeType": "S"},
                                  {"AttributeName": "SK", "AttributeType": "S"}, ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.meta.client.get_waiter('table_exists').wait(TableName="test-card-table")

        mock_event_bridge = MagicMock()
        mock_client.return_value = mock_event_bridge

        bulk_data_mock_response = {
            "data": [
                {"type": "default_cards", "download_uri": "https://data.scryfall.io/default-cards/default-cards-20240116100428.json"}
            ]
        }
        with open('functions/renewEntities/10_cards.json', 'r') as file:
            json_data = json.load(file)
        mock_file_content = json.dumps(json_data).encode('utf-8')

        requests_mock.get("https://api.scryfall.com/bulk-data", json=bulk_data_mock_response)
        requests_mock.get("https://data.scryfall.io/default-cards/default-cards-20240116100428.json", content=mock_file_content)

        # Invoke the lambda handler
        from functions.renewEntities.app import lambda_handler
        lambda_handler({}, {})

        cards = table.scan(
            FilterExpression=Attr("DataType").eq("Card")
        )

        assert requests_mock.called
        assert requests_mock.call_count == 2
        assert len(cards['Items']) == 10

@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table"})
@mock_dynamodb
def test_renew_cards_thirty_cards(requests_mock, table):
    with patch('boto3.client') as mock_client:
        os.environ["DYNAMODB_TABLE_NAME"] = "test-card-table"

        table.meta.client.get_waiter('table_exists').wait(TableName="test-card-table")

        mock_event_bridge = MagicMock()
        mock_client.return_value = mock_event_bridge

        bulk_data_mock_response = {
            "data": [
                {"type": "default_cards", "download_uri": "https://data.scryfall.io/default-cards/default-cards-20240116100428.json"}
            ]
        }
        with open('functions/renewEntities/30_cards.json', 'r') as file:
            json_data = json.load(file)
        mock_file_content = json.dumps(json_data).encode('utf-8')

        requests_mock.get("https://api.scryfall.com/bulk-data", json=bulk_data_mock_response)
        requests_mock.get("https://data.scryfall.io/default-cards/default-cards-20240116100428.json", content=mock_file_content)

        # Invoke the lambda handler
        from functions.renewEntities.app import lambda_handler
        lambda_handler({}, {})

        cards = table.scan(
            FilterExpression=Attr("DataType").eq("Card")
        )

        assert requests_mock.called
        assert requests_mock.call_count == 2
        assert len(cards['Items']) == 30