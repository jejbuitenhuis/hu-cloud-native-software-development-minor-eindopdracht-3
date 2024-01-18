import boto3
import os
import pytest
from moto import mock_dynamodb

DYNAMODB_TABLE_NAME = "test-table"


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto. Otherwise it will deploy it for real"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture()
def setup_dynamodb_collection(aws_credentials):
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
                {"AttributeName": "GSI1SK", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "GSI-Collection-Cards-In-Deck",
                    "KeySchema": [
                        {"AttributeName": "PK", "KeyType": "HASH"},
                        {"AttributeName": "GSI1SK", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1,
                    },
                }
            ],
        )
        yield table


@pytest.fixture()
def setup_dynamodb_collection_with_items(setup_dynamodb_collection):
    table = setup_dynamodb_collection

    table.put_item(
        Item={
            "PK": "USER#test-user",
            "SK": "CardInstance#1Face#1",
            "OracleName": "Bessie, the Doctor's Roadster",
            "OracleText": "Haste Whenever Bessie attacks, another target legendary creature can’t be blocked this turn. Crew 2 (Tap any number of creatures you control with total power 2 or more: This Vehicle becomes an artifact creature until end of turn. ",
            "DataType": "Card",
        },
    )

    table.put_item(
        Item={
            "PK": "USER#test-user",
            "SK": "CardInstance#1#Card",
            "OracleName": "Bessie, the Doctor's Roadster",
            "DataType": "Card",
        },
    )

    yield table
