import logging
import boto3
import time
from src.data_structures.client_group_monitor import ClientGroupMonitor
import traceback


class TimeStreamHandler:
    def __init__(
        self,
        write_client: boto3.client,
        timestream_db: str,
        table_name: str,
        time: str = None,
    ):
        self.write_client = write_client
        self.timestream_db = timestream_db
        self.table_name = table_name
        self.dimensions = []
        self.time = time
        self.processedMetrics = []

    def add_metric(self, name, value, type):
        new_metric = {"Name": name, "Value": value, "Type": type}
        self.processedMetrics.append(new_metric)

    def add_dimension(self, name, value):
        new_dimension = {"Name": name, "Value": str(value)}
        self.dimensions.append(new_dimension)

    def post_new_measure(self, data: ClientGroupMonitor):
        try:
            self.time = str(round(time.time() * 1000))
            self.add_dimension("clientId", data.cleint_id)
            self.add_dimension("groupId", data.group_id)
            self.add_dimension("monitorId", data.monitor_id)
            for measure_name, value in zip(data.variables, data.data):
                self.add_metric(measure_name, str(value), "DOUBLE")
            measure_arrived = {
                "Dimensions": self.dimensions,
                "MeasureName": "MeterMetrics",
                "MeasureValues": self.processedMetrics,
                "MeasureValueType": "MULTI",
                "Time": self.time,
            }
            records = [measure_arrived]
            logging.debug(f"Records to send: {records}")
            result = self.write_client.write_records(
                DatabaseName=self.timestream_db,
                TableName=self.table_name,
                Records=records,
                CommonAttributes={},
            )
            logging.debug(
                "WriteRecords Status: [%s]"
                % result["ResponseMetadata"]["HTTPStatusCode"]
            )
            if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
                logging.debug("A measurement record was added")
                return 200, "A measurement record was added."
            else:
                logging.error("It was not possible to add the measurement record.")
                return 500, "It was not possible to add the measurement record."
        except Exception as err:
            print("Error:", err)
            traceback.print_exc()
            return 500, "It was not possible to add the measurement record."
