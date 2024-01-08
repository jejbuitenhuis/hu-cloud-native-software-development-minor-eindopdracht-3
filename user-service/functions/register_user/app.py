import json
import os
import boto3
from botocore.exceptions import ClientError

client = boto3.client('cognito-idp', region_name='us-east-1')
client_id = os.environ['USER_POOL_CLIENT_ID']
user_pool_id = os.environ['USER_POOL_ID']


def is_email_already_registered(email):
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
            return {
                "status_code": 500,
                "message": str(e)
            }


def lambda_handler(event, context):
    """
        RegisterUserFunction: Lambda function to validate and register a new user in the Cognito User Pool
    """

    print(f'event: {event}')
    print(f'eventtype: {type(event)}')

    body = json.loads(event['body'])

    username = body['username']
    password = body['password']
    email = body['email']

    email_exists = is_email_already_registered(email)

    if email_exists is True:
        return {
            "statusCode": 409,
            "body": json.dumps({
                "message": "This email address is already in use"
            })
        }
    elif email_exists is False:
        response = client.sign_up(
            ClientId=client_id,
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'preferred_username', 'Value': username}
            ]
        )

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "User registered successfully",
                "userSub": response['UserSub']
            })
        }
    else:
        return {
            "statusCode": email_exists["status_code"],
            "body": json.dumps({
                "message": email_exists["message"]
            })
        }

    


    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e