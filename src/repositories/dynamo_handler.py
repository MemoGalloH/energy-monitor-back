import logging


class DynamoHandler:
    def __init__(self, dynamo_table_ref):
        self.table = dynamo_table_ref

    def get_item(self, client_id, client_group_monitor_id):
        try:
            logging.debug("Getting dynamo Item")
            response = self.table.get_item(
                Key={
                    "clientId": client_id,
                    "clientGroupMonitorId": client_group_monitor_id,
                }
            )
            return response.get("Item")
        except Exception as e:
            logging.error(e)
            return None
