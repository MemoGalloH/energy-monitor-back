from src.data_structures.custom_exceptions import (
    NoClientIdUrlError,
    NoClientGroupMonitorIdError,
)
from src.data_structures.client_group_monitor import ClientGroupMonitor
from src.data_structures.custom_exceptions import (
    NoClientIdError,
    NoGroupIdError,
    NoMonitorIdError,
    NoDataError,
)
import json
from decimal import Decimal


def parse_input_measure(event: dict) -> ClientGroupMonitor:
    data = json.loads(event["body"], parse_float=Decimal)
    path_paratmeters = event.get("pathParameters")
    client_id = data.get("clientId")
    if not client_id:
        raise NoClientIdError()
    group_id = data.get("groupId")
    if not group_id:
        raise NoGroupIdError()
    data_measures = data.get("data")
    if not data_measures:
        raise NoDataError()
    monitor_id = path_paratmeters.get("monitorId")
    if not monitor_id:
        raise NoMonitorIdError()

    return ClientGroupMonitor(client_id, group_id, monitor_id, data_measures)


def parse_get_item_client_table(event: dict) -> tuple:
    path_paratmeters = event.get("pathParameters")
    client_id = path_paratmeters.get("clientId")
    if not client_id:
        raise NoClientIdUrlError()
    client_group_monitor_id = path_paratmeters.get("clientGroupMonitorId")
    if not client_group_monitor_id:
        raise NoClientGroupMonitorIdError()
    return client_id, client_group_monitor_id


def parse_table_client_data(data, client_group_monitor_id):
    if client_group_monitor_id != "client":
        if len(client_group_monitor_id.split(".")) > 1:
            parsed_measures = []
            timestamp = None
            for measure in data.get("measures"):
                values = []
                timestamp = int(measure["timestamp"])
                for value in measure["values"]:
                    values.append(float(value))
                parsed_measures.append({"timestamp": timestamp, "values": values})
            data["measures"] = parsed_measures
