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
    logger.info(f"{event} {type(event)}")

    # Cogintio username
    token = event["headers"]["token"]
    claims = jwt.get_unverified_claims(token)
    coginito_username = claims["cognito:username"]
    logger.info(f"Coginito_username: {coginito_username}")

    # Search query
    search_query = event["queryStringParameters"]["q"]
    logger.info(f"Search query {search_query}")
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
