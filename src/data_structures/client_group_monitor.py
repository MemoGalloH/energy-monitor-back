from dataclasses import dataclass, field
from typing import List


@dataclass
class ClientGroupMonitor:
    cleint_id: str = None
    group_id: str = None
    monitor_id: str = None
    data: List = field(default_factory=list)

    def get_client_ref(self):
        return "client"

    def get_group_ref(self):
        return self.group_id

    def get_monitor_ref(self):
        return f"{self.group_id}.{self.monitor_id}"
