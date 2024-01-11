import json
import os
import boto3
from botocore.exceptions import ClientError
from moto import mock_cognitoidp
from unittest.mock import patch


@mock_cognitoidp
def test_lambda_handler_successful():

    # Arrange
    client = boto3.client('cognito-idp', region_name='us-east-1')

    pool_res = client.create_user_pool(
        PoolName='TestUserPool',
        AutoVerifiedAttributes=['email']
    )
    user_pool_id = pool_res['UserPool']['Id']
    print("user_pool_id1:", user_pool_id)

    client_res = client.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName='TestUserPoolClient',
        GenerateSecret=False
    )
    client_id = client_res['UserPoolClient']['ClientId']
    print("client_id1:", client_id)

    event = {
        'body': json.dumps({
            'username': 'testnewuser',
            'password': 'NewPassword456!',
            'email': 'maikel.reijneke@gmail.com'
        })
    }

    os.environ['USER_POOL_CLIENT_ID'] = client_id
    os.environ['USER_POOL_ID'] = user_pool_id  

    from functions.register_user.app import lambda_handler

    # Act
    result = lambda_handler(event, {})

    # Assert
    assert result['statusCode'] == 201
    response_body = json.loads(result['body'])
    response_user = client.admin_get_user(
            UserPoolId=user_pool_id,
            Username='maikel.reijneke@gmail.com'
        )
    assert response_user['UserAttributes'][0]['Value'] == 'testnewuser'


# @mock_cognitoidp
# def test_lambda_handler_email_exists():

#     # Arrange
#     client = boto3.client('cognito-idp', region_name='us-east-1')

#     pool_res = client.create_user_pool(
#         PoolName='TestUserPool2',
#         AutoVerifiedAttributes=['email']
#     )
#     user_pool_id = pool_res['UserPool']['Id']
#     print("user_pool_id2:", user_pool_id)

#     client_res = client.create_user_pool_client(
#         UserPoolId=user_pool_id,
#         ClientName='TestUserPoolClient2',
#         GenerateSecret=False
#     )
#     client_id = client_res['UserPoolClient']['ClientId']
#     print("client_id2:", client_id)

#     client.sign_up(
#         ClientId=client_id,
#         Username='maikel.reijneke@gmail.com',
#         Password='NewPassword456!',
#         UserAttributes=[
#             {'Name': 'preferred_username', 'Value': 'testnewuser'}
#         ]
#     )

#     event = {
#         'body': json.dumps({
#             'username': 'testnewuser',
#             'password': 'NewPassword456!',
#             'email': 'maikel.reijneke@gmail.com'
#         })
#     }
    
#     with patch.dict(os.environ, {
#         'USER_POOL_CLIENT_ID': client_id,
#         'USER_POOL_ID': user_pool_id
#     }):
#         from functions.register_user.app import lambda_handler

#         # Act
#         result = lambda_handler(event, {})

#         # Assert
#         assert result['statusCode'] == 409
#         response_body = json.loads(result['body'])
#         assert response_body['error'] == 'Email address is already in use.'
        

