import importlib
import json
from unittest.mock import patch, MagicMock
import os
import pytest
import boto3
from boto3.dynamodb.conditions import Key
from moto import mock_dynamodb
import logging
import time

logger = logging.getLogger()
logger.setLevel("INFO")

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def setup_table():
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
    return table

@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7",
                         "CARD_JSON_LOCATION": "tests/renew_cards_tests/single_faced_cards.json"})
@mock_dynamodb
def test_renew_cards_writes_correct_data_single_face(requests_mock, aws_credentials):
    # Arrange
    with patch('boto3.client') as mock_client:
        table = setup_table()
        mock_event_bridge = MagicMock()
        mock_client.return_value = mock_event_bridge

        bulk_data_mock_response = {
            "data": [
                {"type": "default_cards", "download_uri": "https://data.scryfall.io/default-cards/default-cards-20240116100428.json"}
            ]
        }
        with open(r'tests/renew_cards_tests/json_test_files/10_cards.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        mock_file_content = json.dumps(json_data).encode('utf-8')

        requests_mock.get("https://api.scryfall.com/bulk-data", json=bulk_data_mock_response)
        requests_mock.get("https://data.scryfall.io/default-cards/default-cards-20240116100428.json", content=mock_file_content)

        # Act
        import functions.renew_entities.app
        importlib.reload(functions.renew_entities.app)
        functions.renew_entities.app.lambda_handler({}, {})

        # Assert
        single_face_card_info = table.query(
            KeyConditionExpression=Key('PK').eq('OracleId#44623693-51d6-49ad-8cd7-140505caf02f') & Key('SK').eq(
                'PrintId#0000579f-7b35-4ed3-b44c-db2a538066fe#Card')
        )

        card = single_face_card_info['Items'][0]
        cardfaces = single_face_card_info['Items'][0]['CardFaces']

        assert requests_mock.called
        assert requests_mock.call_count == 2
        assert len(single_face_card_info['Items']) == 1
        assert card['PK'] == "OracleId#44623693-51d6-49ad-8cd7-140505caf02f"
        assert card['SK'] == "PrintId#0000579f-7b35-4ed3-b44c-db2a538066fe#Card"
        assert card['OracleName'] == "Fury Sliver"
        assert card['SetName'] == "Time Spiral"
        assert card['ReleasedAt'] == "2006-10-06"
        assert card['Rarity'] == "uncommon"
        assert card['Price'] == "0.04"
        assert card['OracleId'] == "44623693-51d6-49ad-8cd7-140505caf02f"
        assert card['PrintId'] == "0000579f-7b35-4ed3-b44c-db2a538066fe"
        assert card['LowerCaseOracleName'] == "fury sliver"

        assert len(cardfaces) == 1
        assert cardfaces[0]['OracleText'] == "All Sliver creatures have double strike."
        assert cardfaces[0]['ManaCost'] == "{5}{R}"
        assert cardfaces[0]['TypeLine'] == "Creature — Sliver"
        assert cardfaces[0]['FaceName'] == "Fury Sliver"
        assert cardfaces[0]['FlavorText'] == "\"A rift opened, and our arrows were abruptly stilled. To move was to push the world. But the sliver's claw still twitched, red wounds appeared in Thed's chest, and ribbons of blood hung in the air.\"\n—Adom Capashen, Benalish hero"
        assert cardfaces[0]['ImageUrl'] == "https://cards.scryfall.io/png/front/0/0/0000579f-7b35-4ed3-b44c-db2a538066fe.png?1562894979"
        assert cardfaces[0]['Colors'] == ["R"]

        os.remove('renew_cards_tests/single_faced_cards.json')


@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7",
                         "CARD_JSON_LOCATION": "tests/renew_cards_tests/two_faced_cards.json"})
@mock_dynamodb
def test_renew_cards_two_faced(requests_mock, aws_credentials):
    # Arrange
    with patch('boto3.client') as mock_client:
        table = setup_table()
        mock_event_bridge = MagicMock()
        mock_client.return_value = mock_event_bridge

        bulk_data_mock_response = {
            "data": [
                {"type": "default_cards", "download_uri": "https://data.scryfall.io/default-cards/default-cards-20240116100428.json"}
            ]
        }
        with open('tests/renew_cards_tests/json_test_files/double_faced_card_list.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        mock_file_content = json.dumps(json_data).encode('utf-8')

        requests_mock.get("https://api.scryfall.com/bulk-data", json=bulk_data_mock_response)
        requests_mock.get("https://data.scryfall.io/default-cards/default-cards-20240116100428.json", content=mock_file_content)

        # Act
        import functions.renew_entities.app
        importlib.reload(functions.renew_entities.app)
        functions.renew_entities.app.lambda_handler({}, {})

        # Assert
        double_face_card_info = table.query(
            KeyConditionExpression=Key('PK').eq('OracleId#562d71b9-1646-474e-9293-55da6947a758') & Key('SK').eq(
                'PrintId#67f4c93b-080c-4196-b095-6a120a221988#Card')
        )


        assert requests_mock.called
        assert requests_mock.call_count == 2

        assert len(double_face_card_info['Items']) == 1
        assert double_face_card_info['Items'][0]['PK'] == "OracleId#562d71b9-1646-474e-9293-55da6947a758"
        assert double_face_card_info['Items'][0]['SK'] == "PrintId#67f4c93b-080c-4196-b095-6a120a221988#Card"
        assert double_face_card_info['Items'][0]['OracleName'] == "Agadeem's Awakening // Agadeem, the Undercrypt"
        assert double_face_card_info['Items'][0]['SetName'] == "Zendikar Rising"
        assert double_face_card_info['Items'][0]['ReleasedAt'] == "2020-09-25"
        assert double_face_card_info['Items'][0]['Rarity'] == "mythic"
        assert double_face_card_info['Items'][0]['Price'] == "18.27"
        assert double_face_card_info['Items'][0]['OracleId'] == "562d71b9-1646-474e-9293-55da6947a758"
        assert double_face_card_info['Items'][0]['PrintId'] == "67f4c93b-080c-4196-b095-6a120a221988"
        assert double_face_card_info['Items'][0]['LowerCaseOracleName'] == "agadeem's awakening // agadeem, the undercrypt"

        cardfaces = double_face_card_info['Items'][0]['CardFaces']
        assert len(cardfaces) == 2
        assert cardfaces[0]['OracleText'] == "Return from your graveyard to the battlefield any number of target creature cards that each have a different mana value X or less."
        assert cardfaces[0]['ManaCost'] == "{X}{B}{B}{B}"
        assert cardfaces[0]['TypeLine'] == "Sorcery"
        assert cardfaces[0]['FaceName'] == "Agadeem's Awakening"
        assert cardfaces[0]['FlavorText'] == '\"Now is the death-hour, just before dawn. Wake, sleepers, and haunt the living!\"\n—Vivias, Witch Vessel'
        assert cardfaces[0]['ImageUrl'] == "https://cards.scryfall.io/png/front/6/7/67f4c93b-080c-4196-b095-6a120a221988.png?1604195226"
        assert cardfaces[0]['Colors'] == ["B"]
        assert cardfaces[0]['LowercaseFaceName'] == "agadeem's awakening"
        assert cardfaces[0]['LowercaseOracleText'] == "return from your graveyard to the battlefield any number of target creature cards that each have a different mana value x or less."

        assert cardfaces[1]['OracleText'] == "As Agadeem, the Undercrypt enters the battlefield, you may pay 3 life. If you don't, it enters the battlefield tapped.\n{T}: Add {B}."
        assert cardfaces[1]['ManaCost'] == ""
        assert cardfaces[1]['TypeLine'] == "Land"
        assert cardfaces[1]['FaceName'] == "Agadeem, the Undercrypt"
        assert cardfaces[1]['FlavorText'] == '\"Here below the hedron fields, souls and secrets lie entombed.\"\n—Vivias, Witch Vessel'
        assert cardfaces[1]['ImageUrl'] == "https://cards.scryfall.io/png/back/6/7/67f4c93b-080c-4196-b095-6a120a221988.png?1604195226"
        assert cardfaces[1]['Colors'] == []
        assert cardfaces[1]['LowercaseFaceName'] == "agadeem, the undercrypt"
        assert cardfaces[1]['LowercaseOracleText'] == "as agadeem, the undercrypt enters the battlefield, you may pay 3 life. if you don't, it enters the battlefield tapped.\n{t}: add {b}."

        os.remove('renew_cards_tests/two_faced_cards.json')


@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7",
                         "CARD_JSON_LOCATION": "tests/renew_cards_tests/ten_cards.json"})
@mock_dynamodb
def test_renew_cards_ten_cards(requests_mock, aws_credentials):
    # Arrange
    with patch('boto3.client') as mock_client:
        table = setup_table()
        mock_event_bridge = MagicMock()
        mock_client.return_value = mock_event_bridge

        bulk_data_mock_response = {
            "data": [
                {"type": "default_cards", "download_uri": "https://data.scryfall.io/default-cards/default-cards-20240116100428.json"}
            ]
        }
        print(f"PWD: {os.getcwd()}")
        with open('tests/renew_cards_tests/json_test_files/10_cards.json', 'r') as file:
            json_data = json.load(file)
        mock_file_content = json.dumps(json_data).encode('utf-8')

        requests_mock.get("https://api.scryfall.com/bulk-data", json=bulk_data_mock_response)
        requests_mock.get("https://data.scryfall.io/default-cards/default-cards-20240116100428.json", content=mock_file_content)

        # Act
        import functions.renew_entities.app
        importlib.reload(functions.renew_entities.app)
        functions.renew_entities.app.lambda_handler({}, {})

        # Assert
        cards = table.scan()

        assert requests_mock.called
        assert requests_mock.call_count == 2
        assert len(cards['Items']) == 10
        os.remove('renew_cards_tests/ten_cards.json')


@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7",
                         "CARD_JSON_LOCATION": "tests/renew_cards_tests/thirty_cards.json"})
@mock_dynamodb
def test_renew_cards_thirty_cards(requests_mock, aws_credentials):
    # Arrange
    with patch('boto3.client') as mock_client:
        table = setup_table()
        mock_event_bridge = MagicMock()
        mock_client.return_value = mock_event_bridge

        bulk_data_mock_response = {
            "data": [
                {"type": "default_cards", "download_uri": "https://data.scryfall.io/default-cards/default-cards-20240116100428.json"}
            ]
        }
        with open('tests/renew_cards_tests/json_test_files/30_cards.json', 'r') as file:
            json_data = json.load(file)
        mock_file_content = json.dumps(json_data).encode('utf-8')

        requests_mock.get("https://api.scryfall.com/bulk-data", json=bulk_data_mock_response)
        requests_mock.get("https://data.scryfall.io/default-cards/default-cards-20240116100428.json", content=mock_file_content)

        # Act
        import functions.renew_entities.app
        importlib.reload(functions.renew_entities.app)
        functions.renew_entities.app.lambda_handler({}, {})

        # Assert
        cards = table.scan()
        assert len(cards['Items']) == 30
        assert requests_mock.called
        assert requests_mock.call_count == 2
        os.remove('renew_cards_tests/thirty_cards.json')


@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMODB_TABLE_NAME": "test-card-table",
                         "CARDS_UPDATE_FREQUENCY" : "7",
                         "CARD_JSON_LOCATION": "tests/renew_cards_tests/correct_ttl.json"})
@mock_dynamodb
def test_renew_cards_has_correct_ttl(requests_mock, aws_credentials):
    # Arrange
    with patch('boto3.client') as mock_client:
        table = setup_table()
        mock_event_bridge = MagicMock()
        mock_client.return_value = mock_event_bridge

        bulk_data_mock_response = {
            "data": [
                {"type": "default_cards", "download_uri": "https://data.scryfall.io/default-cards/default-cards-20240116100428.json"}
            ]
        }
        with open('tests/renew_cards_tests/json_test_files/single_face_card_list.json', 'r') as file:
            json_data = json.load(file)
        mock_file_content = json.dumps(json_data).encode('utf-8')

        requests_mock.get("https://api.scryfall.com/bulk-data", json=bulk_data_mock_response)
        requests_mock.get("https://data.scryfall.io/default-cards/default-cards-20240116100428.json", content=mock_file_content)


        import functions.renew_entities.app
        importlib.reload(functions.renew_entities.app)
        functions.renew_entities.app.lambda_handler({}, {})

        # Assert
        single_face_card = table.query(
            KeyConditionExpression=Key('PK').eq('OracleId#44623693-51d6-49ad-8cd7-140505caf02f')
        )

        CARDS_UPDATE_FREQUENCY = int(os.environ.get('CARDS_UPDATE_FREQUENCY'))*24*60*60

        assert requests_mock.called
        assert requests_mock.call_count == 2
        assert len(single_face_card['Items']) == 1

        for item in single_face_card['Items']:
            print(item['RemoveAt'])
            assert item['RemoveAt'] > int(time.time()) + CARDS_UPDATE_FREQUENCY
            assert item['RemoveAt'] <= int(time.time()) + 2 * CARDS_UPDATE_FREQUENCY
        os.remove('renew_cards_tests/correct_ttl.json')