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

def fetch_api_url():
    LOGGER.info("Fetching api url from ssm")
    try :
        parameter = ssm.get_parameter(Name=f'{STAGE}/MTGCardApi/url')
        return parameter['Parameter']['Value']
    except ClientError as e:
        LOGGER.error(f"Error while fetching api url from ssm: {e}")
        raise e

def parse_card_item(item, user_id, condition):
    card_instance_id = str(uuid.uuid4())
    parts = item["SK"].split("#")
    face_type = parts[-1]
    item_type = '#'.join(parts[2:])

    if (item['DataType'] == 'Card'):
        return {
        "PK": f'UserId#{user_id}',
        "SK": f'CardInstanceId#{card_instance_id}#{item_type}',
        "PrintId": item["PrintId"],
        "CardInstanceId": card_instance_id,
        "Condition": condition,
        "DeckId": "",
        "OracleName": item['OracleName'],
        "SetName": item['SetName'],
        "ReleasedAt": item['ReleasedAt'],
        "Rarity": item['Rarity'],
        "Price": item['Price'],
        "OracleId": item['OracleId'],
        "PrintId": item['PrintId'],
        "DataType": "Card",
        "GSI1SK": ""
    }
    else:
        return {
        "PK": f'UserId#{user_id}',
        "SK": f'CardInstanceId#{card_instance_id}#{item_type}',
        "PrintId": item.get("PrintId", ""),
        "CardInstanceId": card_instance_id,
        "Condition": condition,
        "DeckId": "",
        "OracleText": item['OracleText'],
        "ManaCost": item['ManaCost'],
        "TypeLine": item['TypeLine'],
        "FaceName": item['FaceName'],
        "FlavorText": item['FlavorText'],
        "ImageUrl": item['ImageUrl'],
        "Colors": item['Colors'],
        "FaceType": face_type,
        "DataType": "Face",
        "GSI1SK": "",
    }


def save_card_to_db(items, user_id, condition):
    card_instance_items = []
    try:
        for item in items:
            card_instance_item = parse_card_item(item, user_id, condition)
            COLLECTION_TABLE.put_item(Item=card_instance_item)
            card_instance_items.append(card_instance_item)

    except ClientError as e:
        LOGGER.error(f"Error while saving card instances to the database: {e}")
        raise e
    return card_instance_items



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
        api_url = fetch_api_url()
        api_response = requests.get(f'{api_url}/api/cards/{oracle_id}/{print_id}').json()
        api_response_code = api_response["status_code"]

        if api_response_code != 200:
            LOGGER.error(api_response)
            api_response_body = json.loads(api_response["body"])['Message']
            LOGGER.error(f"Error while fetching card from api: {api_response_code}\n {api_response_body}")
            return {
                "status_code": api_response['status_code'],
                "body": json.dumps({"Message": api_response_body})
            }

        api_response_body = json.loads(api_response["body"])['Items']
        saved_cards = save_card_to_db(api_response_body, user_id, condition)

        LOGGER.info(f"Successfully added the following cards to the collection:")
        for card in saved_cards:
            LOGGER.info(f"{card}\n")
        return {
            "status_code": 201,
            "body": json.dumps({"items": saved_cards})
        }
    except ClientError as e:
        LOGGER.error(f"Error while saving the card: {e}")
        return {
            "status_code": 500,
            "body": json.dumps({"Message": e.response})
        }

