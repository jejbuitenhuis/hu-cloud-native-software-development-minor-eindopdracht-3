import json

import os

from boto3.dynamodb.conditions import Key
from jose import jwt

import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import patch_all
import logging

if 'DISABLE_XRAY' not in os.environ:
    patch_all()

LOGGER = logging.getLogger()
LOGGER.setLevel("INFO")

DYNAMO_DB = boto3.resource("dynamodb", region_name="us-east-1")
DYNAMO_DB_CARD_TABLE_NAME = os.getenv("DYNAMO_DB_CARD_TABLE_NAME")
CARD_TABLE = DYNAMO_DB.Table(DYNAMO_DB_CARD_TABLE_NAME)


def lambda_handler(event, context):
    LOGGER.info("Starting get card from database lambda")

    card_oracle_id = event["oracle_id"]
    card_print_id = event["print_id"]

    try:
        response = CARD_TABLE.query(
                KeyConditionExpression=Key('PK').eq(f"OracleId#{card_oracle_id}")
                & Key('SK').begins_with(f"PrintId#{card_print_id}"))

        if not response["Items"]:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "error": "Card not found."
                })
            }

    except ClientError as e:
        LOGGER.error(f"Error while fetching card: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(e.response)
        }


    LOGGER.info(f'items to be returned: {response["Items"]}')

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
