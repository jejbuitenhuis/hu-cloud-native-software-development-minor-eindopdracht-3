import json
import logging
import boto3
from os import environ
from jose import jwt
from aws_xray_sdk.core import patch_all
from boto3.dynamodb.conditions import Key

if 'DISABLE_XRAY' not in environ:
    patch_all()

logger = logging.getLogger()
logger.setLevel("INFO")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(environ['DYNAMODB_TABLE'])


def lambda_handler(event, context):
    claims = jwt.get_unverified_claims(event['headers']['Authorization'].replace("Bearer ", ""))

    response = table.query(
        KeyConditionExpression=Key('PK').eq(f"USER#{claims['cognito:username']}") & Key('SK').begins_with(f"CardInstanceId#{event['pathParameters']['instance_id']}"),
    )

    if len(response['Items']) == 0:
        return {
            "statusCode": 404
        }

    return {
        "statusCode": 200,
        "body": json.dumps(response['Items']),
    }
