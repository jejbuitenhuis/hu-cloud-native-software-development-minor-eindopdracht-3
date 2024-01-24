import boto3
import logging
import json

from jose import jwt
from aws_xray_sdk.core import patch_all
from os import environ
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

if "DISABLE_XRAY" not in environ:
    patch_all()

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource("dynamodb")
collection_table = dynamodb.Table(environ["DYNAMODB_TABLE"])


def lambda_handler(event, context):
    # Input
    authorization_value = event.get("headers", {}).get("Authorization", None)
    query_string_parameters = event.get("queryStringParameters", {})

    search_value = ""
    last_evaluated_key = None
    limit_value = 40

    search_value = query_string_parameters.get("q", "")

    tmp_last_evaluated_key = query_string_parameters.get("offset")
    tmp_limit = query_string_parameters.get("limit")

    if tmp_last_evaluated_key is not None:
        last_evaluated_key = tmp_last_evaluated_key

    if tmp_limit is not None:
        limit_value = tmp_limit

    logger.info(f"Auth input: {authorization_value}")
    logger.info(f"Search input: {search_value}")

    if not authorization_value:
        return {
            "headers": {
                "Content-Type": "application/json",
            },
            "statusCode": 401,
            "body": json.dumps({"Message": "JWT token not provided"}),
        }

    # Cognito username
    tmp_authorization_value = authorization_value.replace("Bearer ", "")
    logger.info(f"tmp: {tmp_authorization_value}")
    decoded_token = jwt.get_unverified_claims(tmp_authorization_value)
    cognito_username = decoded_token.get("sub")
    logger.info(f"Cognito_username: {cognito_username}")

    # Search query
    search_query = search_value
    search_query = search_query.casefold()
    logger.info(f"Search_query: {search_query}")

    params = {
        "KeyConditionExpression": Key("PK").eq(f"USER#{cognito_username}"),
        "Limit": limit_value,
    }

    if search_query:
        params["FilterExpression"] = (
            Attr("LowerCaseOracleName").contains(search_query)
            | Attr("CombinedLowercaseOracleText").contains(search_query)
            | Attr("LowerCaseOracleName").contains(search_query)
            & Attr("CombinedLowercaseOracleText").contains(search_query)
        )

    if last_evaluated_key:
        params["ExclusiveStartKey"] = last_evaluated_key

    result = collection_table.query(**params)

    logger.info(f"Query success: {result}")
    items = result["Items"]
    logger.info(f"All of the items returned: {items}")

    if not items:
        logger.info("No items found")
        return {
            "headers": {
                "Content-Type": "application/json",
            },
            "statusCode": 404,
            "body": json.dumps({"Message": "Not found"}),
        }

    return {
        "headers": {
            "Content-Type": "application/json",
        },
        "statusCode": 200,
        "body": json.dumps({"Items": items}),
    }
