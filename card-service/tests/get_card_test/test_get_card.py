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

import logging

logger = logging.getLogger()
logger.setLevel("INFO")


def setup_items():
    return [
        {
            "PK": f'OracleId#562d71b9-1646-474e-9293-55da6947a758',
            "SK": f'PrintId#67f4c93b-080c-4196-b095-6a120a221988',
            "OracleId": "562d71b9-1646-474e-9293-55da6947a758",
            "PrintId": "67f4c93b-080c-4196-b095-6a120a221988",
            "OracleName": "Agadeem's Awakening // Agadeem, the Undercrypt",
            "SetName": "Zendikar Rising",
            "ReleasedAt": "2020-09-25",
            "Rarity": "mythic",
            "Price": "18.27",
            "LowerCaseOracleName": "agadeem's awakening // agadeem, the undercrypt",
            "CardFaces": [
                {
                    "PK": f'OracleId#562d71b9-1646-474e-9293-55da6947a758',
                    "SK": f'PrintId#67f4c93b-080c-4196-b095-6a120a221988#Face#1',
                    "OracleId": "562d71b9-1646-474e-9293-55da6947a758",
                    "PrintId": "67f4c93b-080c-4196-b095-6a120a221988",
                    "OracleText": "Return from your graveyard to the battlefield any number of target creature cards that each have a different mana value X or less.",
                    "ManaCost": "{X}{B}{B}{B}",
                    "TypeLine": "Sorcery",
                    "FaceName": "Agadeem's Awakening",
                    "FlavorText": "\"Now is the death-hour, just before dawn. Wake, sleepers, and haunt the living!\"\n—Vivias, Witch Vessel,",
                    "ImageUrl": "https://cards.scryfall.io/png/back/6/7/67f4c93b-080c-4196-b095-6a120a221988.png?1604195226",
                    "Colors": ['B'],
                    "LowercaseFaceName": "agadeem's awakening",
                    "LowercaseOracleText": "return from your graveyard to the battlefield any number of target creature cards that each have a different mana value x or less.",
                },
                {
                    "PK": f'OracleId#562d71b9-1646-474e-9293-55da6947a758',
                    "SK": f'PrintId#67f4c93b-080c-4196-b095-6a120a221988#Face#2',
                    "OracleId": "562d71b9-1646-474e-9293-55da6947a758",
                    "PrintId": "67f4c93b-080c-4196-b095-6a120a221988",
                    "OracleText": "As Agadeem, the Undercrypt enters the battlefield, you may pay 3 life. If you don't, it enters the battlefield tapped.\n{T}: Add {B}.",
                    "ManaCost": "",
                    "TypeLine": "Land",
                    "FaceName": "Agadeem, the Undercrypt",
                    "FlavorText": "\"Here below the hedron fields, souls and secrets lie entombed.\"\n—Vivias, Witch Vessel",
                    "ImageUrl": "https://cards.scryfall.io/png/front/6/7/67f4c93b-080c-4196-b095-6a120a221988.png?1604195226",
                    "Colors": [],
                    "LowercaseFaceName": "agadeem, the undercrypt",
                    "LowercaseOracleText": "as agadeem, the undercrypt enters the battlefield, you may pay 3 life. if you don't, it enters the battlefield tapped.\n{t}: add {b}."
                }
            ]
        }
    ]

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

    return table

@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMO_DB_CARD_TABLE_NAME": "test-card-table"})
@mock_dynamodb
def test_lambda_handler_successful():

    # Arrange
    table = setup_table()

    event = {
        "oracle_id": "562d71b9-1646-474e-9293-55da6947a758",
        "print_id": "67f4c93b-080c-4196-b095-6a120a221988"
    }

    items = setup_items()

    for card in items:
        table.put_item(Item=card)

    import functions.get_card.app
    importlib.reload(functions.get_card.app)

    # Act
    result = functions.get_card.app.lambda_handler(event, {})

    # Assert
    assert result['statusCode'] == 200


@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "EVENT_BUS_ARN": "",
                         "DYNAMO_DB_CARD_TABLE_NAME": "test-card-table"})
@mock_dynamodb
def test_lambda_handler_card_not_found():

    # Arrange
    setup_table()

    event = {
        "oracle_id": "wrong_id",
        "print_id": "wrong_id"
    }

    import functions.get_card.app
    importlib.reload(functions.get_card.app)

    # Act
    result = functions.get_card.app.lambda_handler(event, {})

    # Assert
    assert result['statusCode'] == 404
    response_body = json.loads(result['body'])
    assert response_body['Message'] == 'Card not found.'
