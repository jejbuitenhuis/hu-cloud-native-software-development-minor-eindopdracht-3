import json
from os import environ
import boto3
from aws_xray_sdk.core import patch_all
import logging

if 'DISABLE_XRAY' not in environ:
    patch_all()

event_bus = boto3.client('events')
logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event, context):

    return
