import boto3
import logging
import json

from aws_xray_sdk.core import patch_all
from os import environ
from botocore.exceptions import ClientError

if "DISABLE_XRAY" not in environ:
    patch_all()

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource("dynamodb")
collection_table = dynamodb.Table("Collections")

SEARCH_ATTRIBUTE_NAMES = ["OracleName", "OracleText"]


def lambda_handler(event, context):
    logger.info(f"{event} {type(event)}")

    auth_token = event["headers"]["token"]
    logger.info(f"Auth token: {auth_token}")
    search_query = event["queryStringParameters"]["q"]
    logger.info(f"Search query: {search_query}")

    filter_expression = create_filter_expression(SEARCH_ATTRIBUTE_NAMES)
    logger.info(f"Filter expression query: {filter_expression}")
    attribute_query = create_search_string(search_query)
    logger.info(f"Attribute query: {attribute_query}")

    result = search_for_querystring(
        table=collection_table,
        filter_expression=filter_expression,
        attribute_query=attribute_query,
    )

    if result is None:
        return {
            "statuscode": 404,
            "body": json.dumps({"message": "Not found"}),
            "headers": {
                "Content-Type": "application/json",
            },
        }

    return {"statuscode": 200, "body": json.dumps(result)}


def search_for_querystring(table, filter_expression, attribute_query):
    try:
        table.scan(
            FilterExpression=filter_expression,
            ExpressionAttributeValues=attribute_query,
        )
    except ClientError as e:
        logger.error(f"ClientError occured while scanning, { e }")
        raise
    except:
        logger.error(f"Error occured while scanning, { e }")
        raise


def create_filter_expression(attribute_names) -> str:
    filter_clauses = [f"contains({attr}, :search_string)" for attr in attribute_names]
    filter_expression = " OR ".join(filter_clauses)
    return filter_expression


def create_search_string(query: str):
    return {":search_string": query}
