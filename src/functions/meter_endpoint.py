import os
import logging
import traceback
import boto3
from src.utils.logging_utils import get_log_level
from src.utils.data_classs_utils import parse_imput_measure
from src.repositories.dynamo_handler import DynamoHandler
from src.use_cases.post_new_measure import PostNewMeasure
from src.data_structures.client_group_monitor import ClientGroupMonitor

CLIENT_GROUP_MONITOR_TABLE_NAME = os.environ["CLIENT_GROUP_MONITOR_TABLE_NAME"]
CLIENT = boto3.resource("dynamodb")
CLIENT_GROUP_MONITOR_TABLE = CLIENT.Table(CLIENT_GROUP_MONITOR_TABLE_NAME)
LOG_LEVEL_NAME = os.environ["LOG_LEVEL"]
LOG_LEVEL = get_log_level(LOG_LEVEL_NAME)
logging.getLogger().setLevel(LOG_LEVEL)


def lambda_handler(event, _):
    """body = {"clientId": "string", "groupId": "string}"""
    try:
        logging.debug(event)
        client_Ids = parse_imput_measure(event)
        dynamo_handler = DynamoHandler(CLIENT_GROUP_MONITOR_TABLE)
        use_case = PostNewMeasure(dynamo_handler)
        response = use_case.execute(client_Ids)
    except Exception as e:
        traceback.print_exc()
        logging.error(e)
        return {"statusCode": 500, "body": str(e)}
    return {"statusCode": response["status_code"], "body": response["body"]}
