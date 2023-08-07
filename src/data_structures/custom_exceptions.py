class NoClientIdError(Exception):
    def __init__(self, message="There is no clientId in the body."):
        self.message = message
        super().__init__(self.message)


class NoGroupIdError(Exception):
    def __init__(self, message="There is no groupId in the body."):
        self.message = message
        super().__init__(self.message)


class NoMonitorIdError(Exception):
    def __init__(self, message="There is no monitorId in the URL."):
        self.message = message
        super().__init__(self.message)
