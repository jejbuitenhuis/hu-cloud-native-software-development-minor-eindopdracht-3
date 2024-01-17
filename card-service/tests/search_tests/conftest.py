import boto3
import os
import pytest
from moto import mock_dynamodb

DYNAMODB_TABLE_NAME = "test-card-table"
COGNITO_POOL_NAME = "TestUserPool"
COGNITO_AUTO_VERIFIER_ATTRIBUTES = ["email"]
COGINTO_CLIENT_NAME = "TestUserPoolClient"


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto. Otherwise it will deploy it for real"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture()
@mock_dynamodb
def setup_dynamodb_deck(aws_credentials):
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.create_table(
            TableName=DYNAMODB_TABLE_NAME,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield table


@pytest.fixture()
@mock_dynamodb
def setup_dynamodb_deck_with_item(setup_dynamodb_deck):
    table = setup_dynamodb_deck
    table.put_item(
        Item={
            "PK": {"S": "OracleId#562d71b9-1646-474e-9293-55da6947a758"},
            "SK": {"S": "PrintId#67f4c93b-080c-4196-b095-6a120a221988#Face#2"},
            "OracleName": {"S": "Bessie, the Doctor's Roadster"},
        },
    )

    yield table
