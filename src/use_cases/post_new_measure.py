from src.repositories.dynamo_handler import DynamoHandler
from src.utils.company_ascii_art import COMPANY_ASCII_ART
from src.data_structures.client_group_monitor import ClientGroupMonitor
import logging


class PostNewMeasure:
    def __init__(self, dynamo_handler: DynamoHandler):
        self.dynamo_handler = dynamo_handler

    def execute(self, data: ClientGroupMonitor):
        logging.debug(data)
        status_code = 200
        body = COMPANY_ASCII_ART
        return {"status_code": status_code, "body": body}
