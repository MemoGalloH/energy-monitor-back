from src.repositories.tieme_stream_query_handler import TimeStreamQueryHandler
from src.repositories.dynamo_handler import DynamoHandler
from src.utils.parsing_utils import need_retrieve_data
import traceback
import logging
import json
import os


TIMESTREAM_DB = os.environ["TIMESTREAM_DB"]
TIMESTREAM_MEASURES_TABLE = os.environ["TIMESTREAM_MEASURES_TABLE"]


class GetItemClientTable:
    def __init__(self, dynamo_handler: DynamoHandler):
        self.dynamo_handler = dynamo_handler

    def execute(
        self, client_id, client_group_monitor_id, query_parameters, query_client
    ):
        try:
            logging.debug((client_id, client_group_monitor_id))
            data = self.dynamo_handler.get_item(client_id, client_group_monitor_id)
            if data:
                if need_retrieve_data(client_group_monitor_id):
                    client_group_monitor_id_splitted = client_group_monitor_id.split(
                        "."
                    )
                    group_id = client_group_monitor_id_splitted[0]
                    monitor_id = client_group_monitor_id_splitted[1]
                    print("Rigth place")
                    time_stream_query = TimeStreamQueryHandler(
                        query_client, TIMESTREAM_DB, TIMESTREAM_MEASURES_TABLE
                    )
                    if (
                        query_parameters
                        and query_parameters.get("fd")
                        and query_parameters.get("ld")
                    ):
                        parsed_measures = time_stream_query.get_interval(
                            client_id,
                            group_id,
                            monitor_id,
                            query_parameters.get("fd"),
                            query_parameters.get("ld"),
                            data.get("variables"),
                        )
                    else:
                        parsed_measures = time_stream_query.get_last_day(
                            client_id, group_id, monitor_id, data.get("variables")
                        )
                    data |= {"measures": parsed_measures}
                status_code = 200
                body = json.dumps(data)
            else:
                status_code = 400
                body = "Item not found"
            logging.debug((status_code, body))
        except Exception as e:
            traceback.print_exc()
            status_code = 500
            body = str(e)
        return {"status_code": status_code, "body": body}
