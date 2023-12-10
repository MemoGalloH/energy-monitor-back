from src.repositories.tieme_stream_handler import TimeStreamHandler
from src.repositories.dynamo_handler import DynamoHandler
from src.utils.company_ascii_art import COMPANY_ASCII_ART
from src.data_structures.client_group_monitor import ClientGroupMonitor
import traceback
import logging


class PostNewMeasure:
    def __init__(
        self, dynamo_handler: DynamoHandler, time_stream_handler: TimeStreamHandler
    ):
        self.dynamo_handler = dynamo_handler
        self.time_stream_handler = time_stream_handler

    def execute(self, data: ClientGroupMonitor):
        try:
            logging.debug(data)
            status_code, body = self.dynamo_handler.validate_new_measure(data)
            if status_code:
                status_code, body = self.time_stream_handler.post_new_measure(data)
            logging.debug((status_code, body))
        except Exception as e:
            traceback.print_exc()
            status_code = 500
            body = str(e)
        return {"status_code": status_code, "body": body}
