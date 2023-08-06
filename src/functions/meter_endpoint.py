import os

import boto3

CLIENT_GROUP_MONITOR_TABLE_NAME = os.environ["CLIENT_GROUP_MONITOR_TABLE_NAME"]
CLIENT = boto3.resource("dynamodb")
CLIENT_GROUP_MONITOR_TABLE = CLIENT.Table(CLIENT_GROUP_MONITOR_TABLE_NAME)


def lambda_handler(event, _):
    print(event["body"])

    return {"statusCode": 200, "body": event["body"]}
