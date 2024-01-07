import json
import os
import boto3

client = boto3.client('cognito-idp', region_name='us-east-1')
client_id = os.environ['USER_POOL_CLIENT_ID']


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    username = event['username']
    password = event['password']
    email = event['email']

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
