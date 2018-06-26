import csv
from collections import deque

import of_state_instacnes_new_activitybased.annotate_states as a_s


class AttributeWriterException(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class OFVolumetricAttributeWriter:
    def __init__(self, filename, lst_attributes, flow_info_dict=None, dev_class=None):
        self.filename = filename
        self.attributes = lst_attributes
        self.flow_info_dict = flow_info_dict
        self.device_class = dev_class
        self.instance_interval = 1
        self.counter = 0
        self.last_known_time = None

        self.state_annotator = a_s.AnnotateStates('/Users/Arunan/Documents/PCAP-Transfer/under_process/activity/activity_annotation.txt')

        self.fid = open(filename, 'w')
        self.csv_writer = csv.writer(self.fid)

        self.__prepare_buffer__()
        self.__write_headers__()

    def __prepare_buffer__(self):
        for attribute_name in self.attributes.keys():
            self.attributes[attribute_name]['buffer'] = deque(maxlen=self.attributes[attribute_name]['length'])

    def __write_headers__(self):
        headers = []
        headers.append('tid')
        for e_a in self.attributes.keys():
            headers.append(e_a)

        headers.append('device_label')
        headers.append('states')
        self.csv_writer.writerow(headers)

    def put_reading(self,tid, line_rate, line_counter):
        if self.flow_info_dict is None:
            raise AttributeWriterException('flow_info_dict is None')

        self.counter = self.counter + 1
        self.last_known_time = tid

        for attribute_name in self.attributes.keys():
            flow_name = self.attributes[attribute_name]['flow_col_name']
            flow_id = self.flow_info_dict[flow_name]

            if self.attributes[attribute_name]['src'] == 'rate':
                val = line_rate.get(flow_id, 0)
            elif self.attributes[attribute_name]['src'] == 'count':
                val = line_counter.get(flow_id, 0)

            self.attributes[attribute_name]['buffer'].append(val)

        if (self.counter % self.instance_interval) == 0:
            self.write_row(tid)

    def write_row(self,tid):
        if self.device_class is None:
            raise AttributeWriterException('device class is None')

        attribute_vector = [0] * (len(self.attributes.keys()) + 2)
        attribute_vector[-1] = self.state_annotator.annotate(self.device_class,tid)
        attribute_vector[-2] = self.device_class

        for i,attribute_name in enumerate(self.attributes.keys()):
            attribute_vector[i] = sum(self.attributes[attribute_name]['buffer'])

        if sum(attribute_vector[0:-2]) != 0:  # if it is not an empty instance
            attribute_vector.insert(0,tid)
            self.csv_writer.writerow(attribute_vector)

    def __del__(self):
        self.write_row(self.last_known_time)
        self.fid.close()
