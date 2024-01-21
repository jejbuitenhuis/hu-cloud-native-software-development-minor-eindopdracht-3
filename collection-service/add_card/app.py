import json
import os
import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import patch_all
import logging
from jose import jwt
import requests
import uuid
from os import environ

if 'DISABLE_XRAY' not in environ:
    patch_all()

LOGGER = logging.getLogger()
LOGGER.setLevel("INFO")

DYNAMO_DB = boto3.resource("dynamodb", region_name="us-east-1")
DYNAMO_DB_COLLECTION_TABLE_NAME = os.getenv("DYNAMO_DB_CARD_TABLE_NAME")
COLLECTION_TABLE = DYNAMO_DB.Table(DYNAMO_DB_COLLECTION_TABLE_NAME)
STAGE = os.getenv("STAGE")


ssm = boto3.client('ssm')
api_url = ssm.get_parameter(Name=f'{STAGE}/MTGCardApi/url')


def parse_card_item(item, user_id, condition):



    card_instance_id = uuid.uuid4()

    item_type = item.get("SK").split("#")[2]

    card_instance = {
        "PK": f'UserId#{user_id}',
        "SK": f'CardInstanceId#{card_instance_id}#{item_type}',
        "PrintId": item.get("PrintId", ""),
        "CardInstanceId": card_instance_id,
        "Condition": condition,
        "DataType": item.get("DataType", "")
    }

    return card_instance


def save_card_to_db(items, user_id, condition):
    card_instance_items = []
    try:
        for item in items:
            card_instance_item = parse_card_item(item, user_id, condition)
            COLLECTION_TABLE.put_item(Item=card_instance_item)
            card_instance_items.append(card_instance_item)

    except ClientError as e:
        LOGGER.error(f"Error while saving card instances to the database: {e}")
        return {
            "success": False,
            "database_response": json.dumps(e.response)
        }
    return {
        "success": True,
        "database_response": card_instance_items
    }


def get_user_id(event: dict) -> str:
    token_header: str = event["headers"]["Authorization"]
    if not token_header.startswith("Bearer "):
        raise Exception("Invalid authorization header")

    token_header = token_header[len("Bearer "):]
    claims = jwt.get_unverified_claims(token_header)

    return claims["sub"]


def lambda_handler(event, context):
    LOGGER.info("Starting add card to collection lambda")

    body = json.loads(event["body"])

    oracle_id = body['oracle_id']
    print_id = body['print_id']
    condition = body['condition']
    user_id = get_user_id(event)

    try:
        api_response = requests.get(f'{api_url}/api/cards/{oracle_id}/{print_id}')
        results = api_response.json()

        items = results.get("body")
        response = save_card_to_db(items, user_id, condition)

        if response.get('success'):
            LOGGER.info(f"Successfully added card to the collection")
            return {
                "statusCode": 201,
                "body": response.get("database_response")
            }
        else:
            LOGGER.error(f"Error, database could not write card. Error: {response.get('database_response')}")
            return {
                "statusCode": response['status_code'],
                "body": response.get("body")
            }
    except ClientError as e:
        LOGGER.error(f"Error while sending GET request: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(e.response)
        }

