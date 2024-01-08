import json
import os
import boto3

client = boto3.client('cognito-idp', region_name='us-east-1')
client_id = os.environ['USER_POOL_CLIENT_ID']

import json
from os import environ
import boto3

event_bus = boto3.client('events')

def validate_password(password):
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one uppercase letter.")

    if not any(char.islower() for char in password):
        errors.append("Password must contain at least one lowercase letter.")

    if not any(char.isdigit() for char in password):
        errors.append("Password must contain at least one digit.")

    if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>/?`~" for char in password):
        errors.append("Password must contain at least one special character.")

    return errors


def lambda_handler(event, context):
    """
        RegisterUserFunction: Lambda function to validate and register a new user in the Cognito User Pool
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    print(f'event: {event}')
    print(f'eventtype: {type(event)}')

    body = json.loads(event['body'])

    username = body['username']
    password = body['password']
    email = body['email']

    validation_errors = validate_password(password)

    if validation_errors:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Password validation failed",
                "errors": validation_errors
            })
        }

    response = client.sign_up(
        ClientId=client_id,
        Username=username,
        Password=password,
        UserAttributes=[
            {'Name': 'email', 'Value': email}
        ]
    )

    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": "User registered successfully",
            "userSub": response['UserSub']
            # "location": ip.text.replace("\n", "")
        })
    }
