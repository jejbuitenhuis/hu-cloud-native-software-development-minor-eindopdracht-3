import importlib
from unittest.mock import patch
import os
import boto3
from boto3.dynamodb.conditions import Key
from moto import mock_dynamodb
import logging
import pytest

LOGGER = logging.getLogger()
LOGGER.setLevel("INFO")

test_user_id = "test-user"
table_name = "test-collection-table"

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto. Otherwise it will deploy it for real"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

def setup_table():
    dynamodb = boto3.resource('dynamodb', 'us-east-1')
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'PK', 'KeyType': 'HASH'}, {'AttributeName': 'SK', 'KeyType': 'RANGE'}],
        AttributeDefinitions=[{"AttributeName": "PK", "AttributeType": "S"},
                              {"AttributeName": "SK", "AttributeType": "S"}],
        BillingMode='PAY_PER_REQUEST'
    )
    # Provide the table to the test
    return table

@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "DYNAMODB_TABLE_NAME": table_name,
                         "CARD_JSON_LOCATION": "json_test_files/30_cards.json",
                         "USERID": test_user_id})
@mock_dynamodb
def test_add_many_cards(aws_credentials):
    # Arrange
    table = setup_table()

    # Act
    import functions.add_10000_cards.app
    importlib.reload(functions.add_10000_cards.app)
    functions.add_10000_cards.app.lambda_handler({}, {})

    # Assert
    response = table.scan()

    card = table.query(
        KeyConditionExpression=Key('PK').eq(f'UserId#{test_user_id}'),
        FilterExpression=Key('PrintId').eq('01ce2601-ae94-4ab5-bbd2-65f47281ca28')
    )

    # LOGGER.info(f"Card: {card}")

    assert len(response['Items']) == 30
    assert card['Items'][0]['PrintId'] == '01ce2601-ae94-4ab5-bbd2-65f47281ca28'
    assert card['Items'][0]['Condition'] != None

    assert card['Items'][0]['CardFaces'][0]['OracleText'] == 'Until end of turn, target creature loses all abilities and becomes a red Weird with base power and toughness 0/1.\nFuse (You may cast one or both halves of this card from your hand.)'
    assert card['Items'][0]['CardFaces'][0]['ManaCost'] == '{2}{U}'
    assert card['Items'][0]['CardFaces'][0]['TypeLine'] == 'Instant'
    assert card['Items'][0]['CardFaces'][0]['FaceName'] == 'Turn'
    assert card['Items'][0]['CardFaces'][0]['FlavorText'] == ''
    assert card['Items'][0]['CardFaces'][0]['ImageUrl'] == 'https://cards.scryfall.io/art_crop/front/0/1/01ce2601-ae94-4ab5-bbd2-65f47281ca28.jpg?1544060145'
    assert card['Items'][0]['CardFaces'][0]['Colors'] == ['R', 'U']
    assert card['Items'][0]['CardFaces'][0]['LowercaseFaceName'] == 'turn'
    assert card['Items'][0]['CardFaces'][0]['LowercaseOracleText'] == 'until end of turn, target creature loses all abilities and becomes a red weird with base power and toughness 0/1.\nfuse (you may cast one or both halves of this card from your hand.)'

    assert card['Items'][0]['CardFaces'][1]['OracleText'] == 'Burn deals 2 damage to any target.\nFuse (You may cast one or both halves of this card from your hand.)'
    assert card['Items'][0]['CardFaces'][1]['ManaCost'] == '{1}{R}'
    assert card['Items'][0]['CardFaces'][1]['TypeLine'] == 'Instant'
    assert card['Items'][0]['CardFaces'][1]['FaceName'] == 'Burn'
    assert card['Items'][0]['CardFaces'][1]['FlavorText'] == ''
    assert card['Items'][0]['CardFaces'][1]['ImageUrl'] == 'https://cards.scryfall.io/art_crop/front/0/1/01ce2601-ae94-4ab5-bbd2-65f47281ca28.jpg?1544060145'
    assert card['Items'][0]['CardFaces'][1]['Colors'] == ['R', 'U']
    assert card['Items'][0]['CardFaces'][1]['LowercaseFaceName'] == 'burn'
    assert card['Items'][0]['CardFaces'][1]['LowercaseOracleText'] == 'burn deals 2 damage to any target.\nfuse (you may cast one or both halves of this card from your hand.)'

    # assert False