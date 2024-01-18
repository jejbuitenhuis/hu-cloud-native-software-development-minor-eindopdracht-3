import boto3
import logging
import json

from jose import jwt
from aws_xray_sdk.core import patch_all
from os import environ
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

if "DISABLE_XRAY" not in environ:
    patch_all()

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource("dynamodb")
collection_table = dynamodb.Table("Collections")

SEARCH_ATTRIBUTE_NAMES = ["OracleName", "OracleText"]


def lambda_handler(event, context):
    # Cogintio username
    coginito_username = extract_cognito_username(event["headers"]["Authorization"])

    logger.info(f"Coginito_username: {coginito_username}")

    # Search query
    search_query = event["queryStringParameters"]["q"]
    attribute_query = {":search_string": search_query}
    logger.info(f"Attribute query: {attribute_query}")

    filter_expression = create_filter_expression(SEARCH_ATTRIBUTE_NAMES)
    logger.info(f"Filter expression query: {filter_expression}")

    result = search_for_querystring(
        table=collection_table,
        key_expression=coginito_username,
        filter_expression=filter_expression,
        attribute_query=attribute_query,
    )

    items = result["Items"]

    logger.info(f"All of the items returned: {items}")

    if items is None:
        return {
            "statuscode": 404,
            "body": json.dumps({"message": "Not found"}),
            "headers": {
                "Content-Type": "application/json",
            },
        }

    return {"statuscode": 200, "body": json.dumps()}


def extract_cognito_username(jwt_token):

    decoded_token = jwt.get_unverified_claims(jwt_token)

    # Extract the 'cognito:username' value from the payload
    cognito_username = decoded_token.get("cognito:username")

    return cognito_username
    


def create_filter_expression(attribute_names) -> str:
    filter_clauses = [f"contains({attr}, :search_string)" for attr in attribute_names]
    filter_expression = " OR ".join(filter_clauses)
    return filter_expression


def search_for_querystring(table, key_expression, filter_expression, attribute_query):
    try:
        table.query(
            KeyConditionExpression=Key("PK").eq("USER#" + key_expression),
            FilterExpression=filter_expression,
            ExpressionAttributeValues=attribute_query,
        )
    except ClientError as e:
        logger.error(f"ClientError occured while scanning, { e }")
        raise
    except:
        logger.error(f"Error occured while scanning, { e }")
        raise
