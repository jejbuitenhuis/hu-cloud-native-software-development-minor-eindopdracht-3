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
    card_oracle_id = event["oracle_id"]
    card_print_id = event["print_id"]
    response = table.query(
        KeyConditionExpression=
            Key('PK').eq(f"OracleId#{card_oracle_id}") &
            Key('SK').begins_with(f"PrintId#{card_print_id}"))
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
