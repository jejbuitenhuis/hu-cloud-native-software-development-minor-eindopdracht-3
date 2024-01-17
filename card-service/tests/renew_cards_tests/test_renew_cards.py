import importlib
import json
import time
from unittest.mock import patch, MagicMock
import os
import pytest
import boto3
import requests
import requests_mock
from boto3.dynamodb.conditions import Key, Attr
from moto import mock_dynamodb


def setup_table():
    dynamodb = boto3.resource('dynamodb', 'us-east-1')
    dynamodb.create_table(
        TableName='test-card-table',
        KeySchema=[{'AttributeName': 'PK', 'KeyType': 'HASH'}, {'AttributeName': 'SK', 'KeyType': 'RANGE'}],
        AttributeDefinitions=[{"AttributeName": "PK", "AttributeType": "S"},
                              {"AttributeName": "SK", "AttributeType": "S"}],
        BillingMode='PAY_PER_REQUEST'
    )

    table = boto3.resource("dynamodb").Table('test-card-table')
    table.meta.client.get_waiter('table_exists').wait(TableName="test-card-table")

    # Provide the table to the test
    return table

@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7"})
@mock_dynamodb
def test_renew_cards_writes_correct_data_single_face(requests_mock):
    with patch('boto3.client') as mock_client:
        table = setup_table()
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
        import functions.renewEntities.app
        importlib.reload(functions.renewEntities.app)
        functions.renewEntities.app.lambda_handler({}, {})

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
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7"})
@mock_dynamodb
def test_renew_cards_two_faced(requests_mock):
    with patch('boto3.client') as mock_client:
        table = setup_table()
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
        import functions.renewEntities.app
        importlib.reload(functions.renewEntities.app)
        functions.renewEntities.app.lambda_handler({}, {})

        double_card_faces = table.query(
            KeyConditionExpression=Key('PK').eq('OracleId#562d71b9-1646-474e-9293-55da6947a758')
        )

        assert requests_mock.called
        assert requests_mock.call_count == 2
        assert len(double_card_faces['Items']) == 3




@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7"})
@mock_dynamodb
def test_renew_cards_ten_cards(requests_mock):
    with patch('boto3.client') as mock_client:
        table = setup_table()
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
        import functions.renewEntities.app
        importlib.reload(functions.renewEntities.app)
        functions.renewEntities.app.lambda_handler({}, {})

        cards = table.scan(
            FilterExpression=Attr("DataType").eq("Card")
        )

        assert requests_mock.called
        assert requests_mock.call_count == 2
        assert len(cards['Items']) == 10


@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7"})
@mock_dynamodb
def test_renew_cards_thirty_cards(requests_mock):
    with patch('boto3.client') as mock_client:
        table = setup_table()
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
        import functions.renewEntities.app
        importlib.reload(functions.renewEntities.app)
        functions.renewEntities.app.lambda_handler({}, {})

        cards = table.scan(
            FilterExpression=Attr("DataType").eq("Card")
        )

        assert len(cards['Items']) == 30
        assert requests_mock.called
        assert requests_mock.call_count == 2


@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7"})
@mock_dynamodb
def test_renew_cards_has_correct_ttl(requests_mock):
    with patch('boto3.client') as mock_client:
        table = setup_table()
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
        import functions.renewEntities.app
        importlib.reload(functions.renewEntities.app)
        functions.renewEntities.app.lambda_handler({}, {})

        single_face_card = table.query(
            KeyConditionExpression=Key('PK').eq('OracleId#44623693-51d6-49ad-8cd7-140505caf02f')
        )

        CARDS_UPDATE_FREQUENCY = int(os.environ.get('CARDS_UPDATE_FREQUENCY'))*24*60*60
        print(CARDS_UPDATE_FREQUENCY)
        assert requests_mock.called
        assert requests_mock.call_count == 2
        assert len(single_face_card['Items']) == 2
        for item in single_face_card['Items']:
            print(item['RemoveAt'])
            assert item['RemoveAt'] > int(time.time()) + CARDS_UPDATE_FREQUENCY
            assert item['RemoveAt'] <= int(time.time()) + 2 * CARDS_UPDATE_FREQUENCY


@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7"})
@mock_dynamodb
def test_renew_cards_full():
    with patch('boto3.client') as mock_client:
        table = setup_table()
        mock_event_bridge = MagicMock()
        mock_client.return_value = mock_event_bridge

        # Invoke the lambda handler
        import functions.renewEntities.app
        importlib.reload(functions.renewEntities.app)
        functions.renewEntities.app.lambda_handler({}, {})