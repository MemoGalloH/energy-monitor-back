from dataclasses import dataclass


@dataclass
class ClientGroupMonitor:
    cleint_id: str = None
    group_id: str = None
    monitor_id: str = None
