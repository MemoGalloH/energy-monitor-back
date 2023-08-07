import logging


def get_log_level(log_level_name: str):
    log_level_name = log_level_name.lower()
    print(log_level_name)
    if log_level_name == "debug":
        return logging.DEBUG
    elif log_level_name == "info":
        return logging.INFO
    elif log_level_name == "warning":
        return logging.WARNING
    elif log_level_name == "error":
        return logging.ERROR
    elif log_level_name == "critical":
        return logging.CRITICAL
    else:
        raise ValueError(f"Invalid log level: {log_level_name}")
