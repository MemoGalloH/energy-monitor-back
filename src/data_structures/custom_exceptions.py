class NoClientIdError(Exception):
    def __init__(self, message="There is no clientId in the body."):
        self.message = message
        super().__init__(self.message)


class NoClientIdUrlError(Exception):
    def __init__(self, message="There is no clientId in the URL."):
        self.message = message
        super().__init__(self.message)


class NoClientGroupMonitorIdError(Exception):
    def __init__(self, message="There is no clientGroupMonitorId in the URL."):
        self.message = message
        super().__init__(self.message)


class NoGroupIdError(Exception):
    def __init__(self, message="There is no groupId in the body."):
        self.message = message
        super().__init__(self.message)


class NoDataError(Exception):
    def __init__(self, message="There are no measures in the body."):
        self.message = message
        super().__init__(self.message)


class NoMonitorIdError(Exception):
    def __init__(self, message="There is no monitorId in the URL."):
        self.message = message
        super().__init__(self.message)


class ProcessError(Exception):
    def __init__(self, message="Process error"):
        self.message = message
        super().__init__(self.message)
