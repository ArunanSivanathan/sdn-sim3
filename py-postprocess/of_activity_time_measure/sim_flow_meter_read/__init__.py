import csv


class FlowMeterException(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class FlowMeterReader:
    def __init__(self, file_rate, file_count):
        self.m_file_rate = file_rate
        self.m_file_count = file_count

        self.fid_rate = open(self.m_file_rate)
        self.fid_count = open(self.m_file_count)

        self.csv_rate = csv.reader(self.fid_rate)
        self.csv_count = csv.reader(self.fid_count)

        # Skip header lines
        self.csv_rate.__next__()
        self.csv_count.__next__()

    def __iter__(self):
        return self

    def __next__(self):
        line_rate = self.csv_rate.__next__()
        line_count = self.csv_count.__next__()

        if len(line_rate) == 0 or len(line_count) == 0:
            raise StopIteration

        time_on_rate = line_rate[0]
        time_on_count = line_count[0]

        if time_on_rate != time_on_count:
            raise FlowMeterException("Flow time miss match")

        dict_rate = FlowMeterReader.process_flow_meter(line_rate[1:])
        dict_count = FlowMeterReader.process_flow_meter(line_count[1:])

        return time_on_rate, dict_rate, dict_count

    def process_flow_meter(usage):
        dict_meter = {}
        for e_use in usage:
            str_key_val = e_use.split(":")
            dict_meter[int(str_key_val[0])] = int(str_key_val[1])

        return dict_meter

    def __del__(self):
        self.fid_count.close()
        self.fid_rate.close()
