from _pytest.monkeypatch import MonkeyPatch
import json
import boto3
import uuid
from moto import mock_dynamodb
import unittest

# JWT token {{{
JWT_TOKEN = "eyJraWQiOiJ5cDRXM3o0Rng4Z3FUZ0JDeXh0MkFcLzBZb2Q1Y2hFakd2Sk13MTk3RzhVST0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyYjdlM2VmNS03ZTc4LTQ4NTQtOGFjNS1lZTdmOTRjMDI1ZDUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZTBCVzNWUXJXIiwiY29nbml0bzp1c2VybmFtZSI6IjJiN2UzZWY1LTdlNzgtNDg1NC04YWM1LWVlN2Y5NGMwMjVkNSIsIm9yaWdpbl9qdGkiOiIwZTFhYTA3ZS01YmM4LTQ5NzctOGE3Zi0yMDdlMzQwYzM3YmIiLCJhdWQiOiJtbDlkMnU3YXAzM3Z0dXNhMzl2dnM4bnA1IiwiZXZlbnRfaWQiOiI4YjUwMDk1Zi01YTBlLTRjYTEtOGZiNy1lMjcyNTgxNmQ5NzgiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTcwNTMzMzA3MywiZXhwIjoxNzA1MzM2NjczLCJpYXQiOjE3MDUzMzMwNzMsImp0aSI6IjFlMTNmODg5LWVmYWMtNGU1Ni1iOWRkLWJjMTdhYjRkM2Y1NiIsImVtYWlsIjoiam9yYW0uYnVpdGVuaHVpc0BzdHVkZW50Lmh1Lm5sIn0.Yl9B-63AIRoneShr6-TpyjEpIUuOvg7Tas1NCr8AQpFhFNo4S5eB-6H26JMd3pEawmWaWcNuhmXp7Y8K2IYR6FjLFF2ciUS9B-xNKVLH_9MUWdHqioLdlI39fWFeWDpbNXsF7LMM79H5DTFH_1EwnPNghsZMgNLpFhJtfb4ofoOG0AIG0xQXuYO1tzCHSeIilNbp1W_ITruQEQrqDknxIx98M2tHdxm69m27WPSCVFZaGSJq0GNdCVg7DtYbEzJ20vSn4k-BP6OtdUa7wL_mg5CzWeIUxdCkMixQ8Tnefdi2U9MVJdkoAGo1DRRLS45Hx5uDBkZZJCLRH7-M33LStA"
# }}}

@mock_dynamodb
class TestCreateDeck(unittest.TestCase):
    def get_sut(self):
        from functions.CreateDeck import app

        return app

    def setUp(self):
        self.monkeypatch = MonkeyPatch()

        self.DYNAMO_DB_USER_TABLE_NAME = "table_decks"

        self.monkeypatch.setenv("DISABLE_XRAY", "true")
        self.monkeypatch.setenv("DYNAMO_DB_USER_TABLE_NAME", self.DYNAMO_DB_USER_TABLE_NAME)

        self.dynamodb_client = boto3.client("dynamodb")

        self.dynamodb_client.create_table( # {{{
            TableName=self.DYNAMO_DB_USER_TABLE_NAME,
            KeySchema=[
                {
                    "AttributeName": "PK",
                    "KeyType": "HASH",
                },
                {
                    "AttributeName": "SK",
                    "KeyType": "RANGE",
                },
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "PK",
                    "AttributeType": "S",
                },
                {
                    "AttributeName": "SK",
                    "AttributeType": "S",
                },
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )
        # }}}

        self.sut = self.get_sut()

    def test_deck_is_created(self):
        expected_deck_name = "Test deck"

        mock_event = {
            "body": json.dumps({
                "name": expected_deck_name,
            }),
            "headers": {
                "token": JWT_TOKEN,
            },
        }
        mock_context = {}

        result = self.sut.lambda_handler(mock_event, mock_context)

        assert result["statusCode"] == 201
        assert "body" in result

        body = json.loads(result["body"])

        assert "id" in body
        assert body["id"] != None
        assert body["name"] == expected_deck_name

    def test_invalid_request_is_returned_when_no_body_is_specified(self):
        mock_event = {
            "headers": {
                "token": JWT_TOKEN,
            },
        }
        mock_context = {}

        result = self.sut.lambda_handler(mock_event, mock_context)

        assert result["statusCode"] == 400
        assert "body" in result

        body = json.loads(result["body"])

        assert "message" in body
        assert body["message"] == "Missing 'name'"

    def test_invalid_request_is_returned_when_no_name_is_specified(self):
        mock_event = {
            "body": json.dumps({}),
            "headers": {
                "token": JWT_TOKEN,
            },
        }
        mock_context = {}

        result = self.sut.lambda_handler(mock_event, mock_context)

        assert result["statusCode"] == 400
        assert "body" in result

        body = json.loads(result["body"])

        assert "message" in body
        assert body["message"] == "Missing 'name'"
