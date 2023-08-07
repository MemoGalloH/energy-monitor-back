import os
import logging
import boto3
from src.utils.logging_utils import get_log_level

CLIENT_GROUP_MONITOR_TABLE_NAME = os.environ["CLIENT_GROUP_MONITOR_TABLE_NAME"]
CLIENT = boto3.resource("dynamodb")
CLIENT_GROUP_MONITOR_TABLE = CLIENT.Table(CLIENT_GROUP_MONITOR_TABLE_NAME)
LOG_LEVEL_NAME = os.environ["LOG_LEVEL"]
LOG_LEVEL = get_log_level(LOG_LEVEL_NAME)
logging.getLogger().setLevel(LOG_LEVEL)


def lambda_handler(event, _):
    logging.debug(event["body"])

    return {"statusCode": 200, "body": event["body"]}
