import os
import logging
import traceback
from botocore.config import Config
import boto3
from src.utils.logging_utils import get_log_level
from src.utils.parsing_utils import parse_input_measure
from src.repositories.tieme_stream_handler import TimeStreamHandler
from src.repositories.dynamo_handler import DynamoHandler
from src.use_cases.post_new_measure import PostNewMeasure

CLIENT_GROUP_MONITOR_TABLE_NAME = os.environ["CLIENT_GROUP_MONITOR_TABLE_NAME"]
REGION_NAME = os.environ["AWS_REGION"]
CLIENT = boto3.resource("dynamodb")
CLIENT_GROUP_MONITOR_TABLE = CLIENT.Table(CLIENT_GROUP_MONITOR_TABLE_NAME)
LOG_LEVEL_NAME = os.environ["LOG_LEVEL"]
LOG_LEVEL = get_log_level(LOG_LEVEL_NAME)
TIMESTREAM_DB = os.environ["TIMESTREAM_DB"]
TIMESTREAM_MEASURES_TABLE = os.environ["TIMESTREAM_MEASURES_TABLE"]
logging.getLogger().setLevel(LOG_LEVEL)


session = boto3.Session()
write_client = session.client(
    "timestream-write",
    config=Config(
        region_name=REGION_NAME,
        read_timeout=20,
        max_pool_connections=5000,
        retries={"max_attempts": 10},
    ),
)


def lambda_handler(event, _):
    """body = {
        "clientId": String,
        "groupId": String,
        "data": List[float],
    }"""
    try:
        logging.debug(event)
        client_Ids = parse_input_measure(event)
        time_stream_handler = TimeStreamHandler(
            write_client, TIMESTREAM_DB, TIMESTREAM_MEASURES_TABLE
        )
        dynamo_handler = DynamoHandler(CLIENT_GROUP_MONITOR_TABLE)
        use_case = PostNewMeasure(dynamo_handler, time_stream_handler)
        response = use_case.execute(client_Ids)
    except Exception as e:
        traceback.print_exc()
        logging.error(e)
        return {"statusCode": 500, "body": str(e)}
    return {"statusCode": response["status_code"], "body": response["body"]}
