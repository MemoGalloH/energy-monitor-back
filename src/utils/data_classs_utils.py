from src.data_structures.client_group_monitor import ClientGroupMonitor
from src.data_structures.custom_exceptions import (
    NoClientIdError,
    NoGroupIdError,
    NoMonitorIdError,
)
import json


def parse_imput_measure(event: dict) -> ClientGroupMonitor:
    data = json.loads(event["body"])
    path_paratmeters = event.get("pathParameters")
    client_id = data.get("clientId")
    if not client_id:
        raise NoClientIdError()
    group_id = data.get("groupId")
    if not group_id:
        raise NoGroupIdError()
    monitor_id = path_paratmeters.get("monitor_id")
    if not monitor_id:
        raise NoMonitorIdError()

    return ClientGroupMonitor(client_id, group_id, monitor_id)
