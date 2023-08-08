from src.repositories.dynamo_handler import DynamoHandler
from src.utils.parsing_utils import parse_table_client_data
import traceback
import logging
import json


class GetItemClientTable:
    def __init__(self, dynamo_handler: DynamoHandler):
        self.dynamo_handler = dynamo_handler

    def execute(self, client_id, client_group_monitor_id):
        try:
            logging.debug((client_id, client_group_monitor_id))
            data = self.dynamo_handler.get_item(client_id, client_group_monitor_id)
            if data:
                parse_table_client_data(data, client_group_monitor_id)
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
