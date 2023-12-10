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

            a = [
                {
                    "Dimensions": [
                        {"Name": "clientId", "Value": "1053779590"},
                        {
                            "Name": "groupId",
                            "Value": "74f9ae48-36ce-4b4e-bdd3-3899fa886b02",
                        },
                        {
                            "Name": "monitorId",
                            "Value": "796b2cc2-b848-4e16-bf17-ff506b5d0602",
                        },
                    ],
                    "MeasureName": "MeterMetrics",
                    "MeasureValues": [
                        {"Name": "V_A", "Value": "20.5", "Type": "DOUBLE"},
                        {"Name": "I_A", "Value": "120.34", "Type": "DOUBLE"},
                        {"Name": "PA_A", "Value": "117.28", "Type": "DOUBLE"},
                        {"Name": "EA_A_I", "Value": "121.43", "Type": "DOUBLE"},
                        {"Name": "F", "Value": "300.33", "Type": "DOUBLE"},
                        {"Name": "FP_A", "Value": "304.33", "Type": "DOUBLE"},
                    ],
                    "MeasureValueType": "MULTI",
                    "Time": "1702241361",
                }
            ]

            return 500, "It was not possible to add the measurement record."
