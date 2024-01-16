import os
from unittest.mock import patch
from conftest import setup_dynamodb_collection, setup_cognito
from moto import mock_dynamodb, mock_cognitoidp

COGINTO_USERNAME = 'test@example.com'
COGINTO_PASSWORD = 'NewPassword456!'

@patch.dict(os.environ, {"DISABLE_XRAY": "True", "EVENT_BUS_ARN": ""})
@mock_dynamodb
@mock_cognitoidp
def test_search_works():
    
    from functions.Search.app import lambda_handler
    
    # Arrange 
    dynamo_client, table_name = setup_dynamodb_collection()
    cognito_client, user_pool_id, user_pool_client_id = setup_cognito()
    
    cognito_client.sign_up(
        ClientId=user_pool_client_id,
        Username=COGINTO_USERNAME,
        Password=COGINTO_PASSWORD,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': COGINTO_USERNAME
            }
        ]
    )

    cognito_client.admin_confirm_sign_up(
        UserPoolId=user_pool_id,
        Username=COGINTO_USERNAME
    )

    dynamo_client.put_item(
        TableName=table_name,
        Item={
            
        }
    )
    
    event = {
        'headers': {'Authorization': 'valid_id_token'},
        'queryStringParameters': {'q': 'doctor'}
    }
    
    # Act
    result = lambda_handler(event, None)
    
    # Assert
    expected_output = {
        'statuscode': 200,
        'body': '{"item": "result"}'
    }
     
    assert result == expected_output


@patch.dict(os.environ, {"DISABLE_XRAY": "True", "EVENT_BUS_ARN": ""})
@mock_cognitoidp
def test_search_invalid_token():
    
    from functions.Search.app import lambda_handler
    
    # Arrange 
    setup_cognito()

    event = {
        'headers': {'Authorization': 'invalid_token'},
        'queryStringParameters': {'q': 'doctor'}
    }

    # Act
    result = lambda_handler(event, None)
    
    # Assert
    expected_output = {
        'statuscode': 401,
        'error': 'Invalid authorization token',
        'message': 'The provided token is either expired or incorrect. Please authenticate and try again.'
    }
    
    assert result == expected_output

@patch.dict(os.environ, {"DISABLE_XRAY": "True", "EVENT_BUS_ARN": ""})
@mock_dynamodb
@mock_cognitoidp
def test_search_not_found():
    
    from functions.Search.app import lambda_handler
    
    # Arrange 
    setup_dynamodb_collection()
    cognito_client, user_pool_id, user_pool_client_id = setup_cognito()
    
    cognito_client.sign_up(
        ClientId=user_pool_client_id,
        Username=COGINTO_USERNAME,
        Password=COGINTO_PASSWORD,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': COGINTO_USERNAME
            }
        ]
    )

    cognito_client.admin_confirm_sign_up(
        UserPoolId=user_pool_id,
        Username=COGINTO_USERNAME
    )

    event = {
        'headers': {'Authorization': 'valid_id_token'},
        'queryStringParameters': {'q': 'invalid'}
    }
    
    # Act
    result = lambda_handler(event, None)
    
    # Assert
    expected_output = {
        'statuscode': 404,
        'body': '',
    }
     
    assert result == expected_output

