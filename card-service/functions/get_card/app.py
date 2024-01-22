import json
import logging
import boto3
from os import environ
from aws_xray_sdk.core import patch_all
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

if 'DISABLE_XRAY' not in environ:
    patch_all()

LOGGER = logging.getLogger()
LOGGER.setLevel("INFO")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(environ['DYNAMODB_TABLE_NAME'])


def lambda_handler(event, context):
    card_oracle_id = event["pathParameters"]["oracle_id"]
    card_print_id = event["pathParameters"]["print_id"]

    try:
        response = table.query(
            KeyConditionExpression=
            Key('PK').eq(f"OracleId#{card_oracle_id}") &
            Key('SK').begins_with(f"PrintId#{card_print_id}"))

        if not response["Items"]:
            return {
                "status_code": 404,
                "body": json.dumps({
                    "Message": "Card not found."
                })
            }

    except ClientError as e:
        LOGGER.error(f"Error while fetching card: {e}")
        return {
            "status_code": 500,
            "body": json.dumps({"Message": "Server error while fetching card."})
        }

    LOGGER.info(f'items to be returned: {response["Items"]}')

    return {
        "status_code": 200,
        "body": json.dumps({"Items": response['Items']})
    }
