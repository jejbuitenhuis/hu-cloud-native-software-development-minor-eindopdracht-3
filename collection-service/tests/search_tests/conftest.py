import boto3
import os
import pytest

DYNAMODB_TABLE_NAME = "collection"
COGNITO_POOL_NAME = "TestUserPool"
COGNITO_AUTO_VERIFIER_ATTRIBUTES = ['email']
COGINTO_CLIENT_NAME = "TestUserPoolClient"

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto. Otherwise it will deploy it for real"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'


@pytest.fixture
def setup_dynamodb_collection(aws_credentials):
    client = boto3.client('dynamodb')
    client.create_table(
        TableName=DYNAMODB_TABLE_NAME,
    )

    return client, DYNAMODB_TABLE_NAME


@pytest.fixture
def setup_cognito(aws_credentials):
    client = boto3.client('cognito-idp')

    pool_res = client.create_user_pool(
        PoolName=COGNITO_POOL_NAME,
        AutoVerifiedAttributes=COGNITO_AUTO_VERIFIER_ATTRIBUTES,
    )
    user_pool_id = pool_res['UserPool']['Id']

    client_res = client.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName=COGINTO_CLIENT_NAME,
        GenerateSecret=False
    )
    user_pool_client_id = client_res['UserPoolClient']['ClientId']

    return client, user_pool_id, user_pool_client_id