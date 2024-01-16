import boto3
from aws_xray_sdk.core import patch_all
import logging
from os import environ
import json

if "DISABLE_XRAY" not in environ:
    patch_all()

logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event, context):
    return result


def search_in_dynamodb(query):
    # TODO
    pass


def extract_user_info(id_token):
    # TODO
    pass
