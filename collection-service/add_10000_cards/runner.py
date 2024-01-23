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


# !--------------------UPDATE user_id DEPENDING ON THE USER--------------------!
user_id = "test-user"
# !--------------------UPDATE table_name DEPENDING ON THE STACK--------------------!
table_name = "10000-cards-mtg-collection-db"

@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "DYNAMODB_TABLE_NAME": table_name,
                         "CARD_JSON_LOCATION": r"D:\GitHub\hu-cloud-native-software-development-minor-eindopdracht-3\collection-service\tests\add_10000_cards_test\json_test_files\default-cards.json",
                         "USERID": user_id})
def test_add_many_cards():
    import add_10000_cards.app
    importlib.reload(add_10000_cards.app)
    add_10000_cards.app.lambda_handler({}, {})