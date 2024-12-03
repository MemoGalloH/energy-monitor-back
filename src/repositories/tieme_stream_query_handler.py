import traceback
from datetime import datetime


class TimeStreamQueryHandler:
    def __init__(self, client, database_name, table_name):
        self.client = client
        self.paginator = client.get_paginator("query")
        self.database_name = database_name
        self.table_name = table_name

    def get_last_day(self, client_id, group_id, monitor_id, variables):
        query = (
            "SELECT time, " + ", ".join(variables) + " "
            "FROM "
            + '"'
            + self.database_name
            + '"'
            + "."
            + '"'
            + self.table_name
            + '"'
            + " "
            "WHERE clientId=" + "'" + client_id + "'" + " "
            "AND groupId=" + "'" + group_id + "'" + " "
            "AND monitorId=" + "'" + monitor_id + "'" + " "
            "AND time between ago(24h) and now() ORDER BY time DESC"
            ""
        )
        return self.run_query(query)

    def get_interval(self, client_id, group_id, monitor_id, fd, ld, variables):
        query = (
            "SELECT time, " + ", ".join(variables) + " "
            "FROM "
            + '"'
            + self.database_name
            + '"'
            + "."
            + '"'
            + self.table_name
            + '"'
            + " "
            "WHERE clientId=" + "'" + client_id + "'" + " "
            "AND groupId=" + "'" + group_id + "'" + " "
            "AND monitorId=" + "'" + monitor_id + "'" + " "
            "AND time BETWEEN TIMESTAMP '"
            + fd
            + "' AND TIMESTAMP '"
            + ld
            + "' ORDER BY time DESC"
            ""
        )
        return self.run_query(query)

    def get_last_24_measures(self, client_id, group_id, monitor_id, variables):
        query = (
            "SELECT time, " + ", ".join(variables) + " "
            "FROM "
            + '"'
            + self.database_name
            + '"'
            + "."
            + '"'
            + self.table_name
            + '"'
            + " "
            "WHERE clientId=" + "'" + client_id + "'" + " "
            "AND groupId=" + "'" + group_id + "'" + " "
            "AND monitorId=" + "'" + monitor_id + "'" + " "
            "ORDER BY time DESC "
            "LIMIT 24"
        )
        return self.run_query(query)

    def run_query(self, query_string):
        try:
            page_iterator = self.paginator.paginate(QueryString=query_string)
            parsed_measures = []
            for page in page_iterator:
                parsed_measures += self.__parse_query_result(page)
            return parsed_measures
        except Exception as err:
            print("Exception while running query:", err)
            traceback.print_exc()
            return None

    def __parse_query_result(self, query_result):
        parsed_measures = []
        for row in query_result["Rows"]:
            parsed_measures.append(self.__parse_row(row))
        return parsed_measures

    def __parse_row(self, row):
        data = row["Data"]
        values = []
        for j in range(1, len(data)):
            values.append(
                data[j].get("ScalarValue"),
            )
        timestamp = datetime.strptime(
            data[0].get("ScalarValue").split(".")[0], "%Y-%m-%d %H:%M:%S"
        )
        return {"timestamp": int(datetime.timestamp(timestamp)), "values": values}
