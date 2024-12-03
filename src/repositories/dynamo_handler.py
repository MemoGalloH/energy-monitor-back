import logging
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

    def validate_new_measure(self, data: ClientGroupMonitor):
        isTheredata = self.get_item(data.cleint_id, data.get_monitor_ref())
        if isTheredata:
            monitorItem = MonitorItem(**isTheredata)
            if monitorItem.isActive:
                if len(monitorItem.variables) == len(data.data):
                    data.variables = monitorItem.variables
                    logging.debug("Measure is valid.")
                    return 200, "Measure is valid"
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
