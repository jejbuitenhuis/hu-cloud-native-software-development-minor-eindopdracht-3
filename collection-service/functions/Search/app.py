import boto3
from aws_xray_sdk.core import patch_all
import logging
from os import environ
import json

# from botocore.exceptions import

if "DISABLE_XRAY" not in environ:
    patch_all()

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource("dynamodb")
collection_table = dynamodb.table("Collection")


def lambda_handler(event, context):
    logger.info(f"{event} {type(event)}")

    search_query = event["queryStringParameters"]["q"]
    logger.info(f"Search query: {search_query}")

    # Step 1 get the user that is searching
    # Step 2 get the search query
    # Step 3 do a scan on
    # Step 4 if


def search_in_dynamodb(table, query):
    # TODO
    pass
