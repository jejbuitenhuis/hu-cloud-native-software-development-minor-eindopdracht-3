import json
from os import environ
import boto3

event_bus = boto3.client('events')


def lambda_handler(event, context):
    event = {
        'Source': 'user-context',
        'DetailType': 'PingEvent',
        'Detail': json.dumps({
            "message": "Ping!"
        }),
        'EventBusName': environ['EVENT_BUS_ARN']
    }
    event_bus.put_events(Entries=[event])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Pong",
        }),
    }
