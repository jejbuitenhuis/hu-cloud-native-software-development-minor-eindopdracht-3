import json
import os
import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import patch_all
import logging
import datetime

patch_all()

logger = logging.getLogger()
logger.setLevel("INFO")

client = boto3.client('cognito-idp', region_name='us-east-1')


def is_email_already_registered(email, user_pool_id):
    try:
        response = client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=email
        )
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "UserNotFoundException":
            return False
        else:
            logger.error(e.response)
            return e.response



def lambda_handler(event, context):
    """
        RegisterUserFunction: Lambda function to validate and register a new user in the Cognito User Pool
    """
    client_id = os.environ['USER_POOL_CLIENT_ID']
    user_pool_id = os.environ['USER_POOL_ID']

    logger.info(f'EventType: {type(event)}')
    logger.info(f'Event: {event}')
    
    logger.info(f'Client: {client}')
    logger.info(f'ClientID: {client_id}')
    logger.info(f'UserPoolID: {user_pool_id}')

    body = json.loads(event['body'])

    # username = body['username']
    password = body['password']
    email = body['email']

    email_exists = is_email_already_registered(email, user_pool_id)
    email_used_str = 'Email address is already in use.'

    if email_exists is True:
        logger.info(email_used_str)
        return {
            "statusCode": 409,
            "body": json.dumps({
                "error": email_used_str
            })
        }
    elif email_exists is False:
        logger.info("Email address is not registered. Proceeding with user registration.")

        try:
            response = client.sign_up(
                ClientId=client_id,
                Username=email,
                Password=password,
                # UserAttributes=[
                #     {'Name': 'preferred_username', 'Value': username}
                # ]
            )
        except ClientError as e:
            logger.error(e.response)
            return e.response
            

        logger.info(f'User Registered: {response}')

        return {
            "statusCode": 201,
            "body": json.dumps(response)
        }
    else:
        return email_exists


    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e