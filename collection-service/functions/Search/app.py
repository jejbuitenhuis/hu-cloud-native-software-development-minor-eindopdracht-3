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
    # Cognito username
    decoded_token = jwt.get_unverified_claims(event["headers"]["Authorization"])
    cognito_username = decoded_token.get("cognito:username")
    logger.info(f"Cognito_username: {cognito_username}")

    # Search query
    search_query = event["queryStringParameters"]["q"]
    search_query = search_query.casefold()
    logger.info(f"Search_query: {search_query}")

    result = search_for_querystring(
        table=collection_table,
        key_expression=cognito_username,
        search_query=search_query,
    )

    logger.info(f"Query success: {result}")
    items = result["Items"]
    logger.info(f"All of the items returned: {items}")

    if not items:
        return {
            "headers": {
                "Content-Type": "application/json",
            },
            "statuscode": 404,
            "body": json.dumps({"message": "Not found"}),
        }

    return {
        "headers": {
            "Content-Type": "application/json",
        },
        "statuscode": 200,
        "body": json.dumps({"Items": items}),
    }


def search_for_querystring(table, key_expression, search_query):
    try:
        return table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{key_expression}"),
            FilterExpression=
            # # Facename and OracleText
            Attr("Facename").contains(search_query)
            & Attr("OracleText").contains(search_query)
            # OracleName
            | Attr("OracleName").contains(search_query),
            ExpressionAttributeValues={":query": search_query},
        )
    except ClientError as e:
        logger.error(f"ClientError occured while scanning, { e }")
        raise
    except:
        logger.error(f"Error occured while scanning, { e }")
        raise
