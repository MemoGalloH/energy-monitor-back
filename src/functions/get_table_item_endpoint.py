import os
import logging
import traceback
import boto3
from src.utils.logging_utils import get_log_level
from src.utils.parsing_utils import parse_get_item_client_table
from src.repositories.dynamo_handler import DynamoHandler
from src.use_cases.get_item_client_table import GetItemClientTable

CLIENT_GROUP_MONITOR_TABLE_NAME = os.environ["CLIENT_GROUP_MONITOR_TABLE_NAME"]
CLIENT = boto3.resource("dynamodb")
CLIENT_GROUP_MONITOR_TABLE = CLIENT.Table(CLIENT_GROUP_MONITOR_TABLE_NAME)
LOG_LEVEL_NAME = os.environ["LOG_LEVEL"]
LOG_LEVEL = get_log_level(LOG_LEVEL_NAME)
logging.getLogger().setLevel(LOG_LEVEL)


def lambda_handler(event, _):
    try:
        logging.debug(event)
        client_Id, client_group_monitor_id = parse_get_item_client_table(event)
        dynamo_handler = DynamoHandler(CLIENT_GROUP_MONITOR_TABLE)
        use_case = GetItemClientTable(dynamo_handler)
        response = use_case.execute(client_Id, client_group_monitor_id)
    except Exception as e:
        traceback.print_exc()
        logging.error(e)
        return {"statusCode": 500, "body": str(e)}
    return {
        "statusCode": response["status_code"],
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": response["body"],
    }
