import importlib
from unittest.mock import patch
import os
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel("INFO")


# !--------------------UPDATE user_id DEPENDING ON THE USER--------------------!
user_id = "test-user"
# !--------------------UPDATE table_name DEPENDING ON THE STACK--------------------!
table_name = "10000-cards-mtg-collection-db"
# !--------------------UPDATE default-cards_json_path DEPENDING ON THE PATH--------------------!
default_cards_json_path = r""

@patch.dict(os.environ, {"DISABLE_XRAY": "True",
                         "DYNAMODB_TABLE_NAME": table_name,
                         "CARD_JSON_LOCATION": default_cards_json_path,
                         "USERID": user_id})
def test_add_many_cards():
    import add_10000_cards.app
    importlib.reload(add_10000_cards.app)
    add_10000_cards.app.lambda_handler({}, {})