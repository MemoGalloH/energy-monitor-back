import logging
from datetime import datetime, timezone
from src.data_structures.client_group_monitor import ClientGroupMonitor, MonitorItem


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
            monitorItem = MonitorItem(**isTheredata)
            if monitorItem.isActive:
                if len(monitorItem.variables) == len(data.data):
                    dt = datetime.now(timezone.utc)
                    utc_time = dt.replace(tzinfo=timezone.utc)
                    utc_timestamp = int(utc_time.timestamp())
                    measure = {"timestamp": utc_timestamp, "values": data.data}
                    response = self.table.update_item(
                        Key={
                            "clientId": monitorItem.clientId,
                            "clientGroupMonitorId": monitorItem.clientGroupMonitorId,
                        },
                        UpdateExpression="set #measures = list_append(#measures, :measure)",
                        ExpressionAttributeNames={"#measures": "measures"},
                        ExpressionAttributeValues={":measure": [measure]},
                        ReturnValues="UPDATED_NEW",
                    )
                    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        logging.debug("A measurement record was added")
                        return 200, "A measurement record was added."
                else:
                    logging.error(
                        "Non-coincidence between the number of measurements received and expected."
                    )
                    return (
                        500,
                        "Non-coincidence between the number of measurements received and expected.",
                    )
            else:
                logging.error("The monitor is not active.")
                return 500, "The monitor is not active."
        else:
            logging.error("There are no records in the database for this monitor.")
            return 500, "There are no records in the database for this monitor."
