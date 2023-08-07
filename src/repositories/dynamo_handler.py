import logging
from datetime import datetime, timezone
from src.data_structures.client_group_monitor import ClientGroupMonitor
from src.data_structures.custom_exceptions import ProcessError
from decimal import Decimal


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

    def put_new_measure(self, data: ClientGroupMonitor):
        isTheredata = self.get_item(data.cleint_id, data.get_monitor_ref())
        if isTheredata:
            dt = datetime.now(timezone.utc)
            utc_time = dt.replace(tzinfo=timezone.utc)
            utc_timestamp = int(utc_time.timestamp())
            measure = {"timestamp": utc_timestamp, "values": data.data}
            response = self.table.update_item(
                Key={
                    "clientId": data.cleint_id,
                    "clientGroupMonitorId": data.get_monitor_ref(),
                },
                UpdateExpression="set #measures = list_append(#measures, :measure)",
                ExpressionAttributeNames={"#measures": "measures"},
                ExpressionAttributeValues={":measure": [measure]},
                ReturnValues="UPDATED_NEW",
            )
            return response
        else:
            raise ProcessError("There are no records in the database for this monitor.")
