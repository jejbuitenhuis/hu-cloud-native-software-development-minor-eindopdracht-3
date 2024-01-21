import json
import logging
import boto3
from os import environ
from aws_xray_sdk.core import patch_all
from boto3.dynamodb.conditions import Key

if 'DISABLE_XRAY' not in environ:
    patch_all()

logger = logging.getLogger()
logger.setLevel("INFO")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(environ['DYNAMODB_TABLE_NAME'])


def lambda_handler(event, context):
    response = table.query(
        IndexName="Card-Id-GSI",
        KeyConditionExpression=Key('GSI1PK').eq(f"PrintId#{event['pathParameters']['card_id']}"),
    )
    items = response['Items']

    if len(items) == 0:
        return {
            "statusCode": 404
        }

    for item in items:
        item.pop('RemoveAt', None)

    return {
        "statusCode": 200,
        "body": json.dumps(items),
        "headers": {
            "content-type": "application/json"
        },
        "isBase64Encoded": False
    }
