import csv
import os
from of_activity_time_measure.executesim import execute_sim
import of_activity_time_measure.config as cfg
import of_activity_time_measure.sim_flow_info_read as f_info
import of_activity_time_measure.sim_flow_meter_read as f_meter
from of_activity_time_measure.of_volumetric_attribute_writer import OFVolumetricAttributeWriter
import of_activity_time_measure.annotate_states as a_s

def read_volumetric_attributes(config_dict):
    instance_out_file = config_dict['instance_out_file']
    flow_info_file = config_dict['flow_info_file']
    device_info = config_dict['device_info']
    gateway_mac = config_dict['gateway']
    flow_meter_rate_file = config_dict['flow_meter_rate_file']
    flow_meter_count_file = config_dict['flow_meter_count_file']
    attribute_info = config_dict['attribute_info']
    tcam_rules_gen_function = config_dict['tcam_rules_gen_function']
    annotation_offset = config_dict['annotation_offset']
    annotation_files = config_dict['annotation_files']


    flow_info = f_info.FlowInfoReader(flow_info_file)

    attribute_writer = OFVolumetricAttributeWriter(instance_out_file, attribute_info)
    state_annotator = a_s.AnnotateStates(annotation_files,annotation_offset)

    for e_device in device_info:
        print(e_device['class'])

        dev_flows = flow_info.find_device_flows(tcam_rules_gen_function(e_device['mac'], gateway_mac))
        attribute_writer.flow_info_dict = dev_flows

        flow_meter = f_meter.FlowMeterReader(flow_meter_rate_file, flow_meter_count_file)

        for tid, dict_rate, dict_count in flow_meter:
            labels = [e_device['class'],state_annotator.annotate(e_device['class'],tid)]
            attribute_writer.put_reading(tid, dict_rate, dict_count,labels)

def write_flowentryfiles():
    fid = open('./executesim/flowentries.csv','w')
    csv_writer = csv.writer(fid)

    headers = ['eth_src', 'eth_dst', 'eth_type', 'ip_tos', 'ip_p', 'ip_src', 'ip_dst', 'port_src', 'port_dst']
    csv_writer.writerow(headers)

    for e_d in cfg.DEVICE_DICT:
        up_flow = [e_d['mac'], ' * ', ' * ', ' * ', ' * ', ' * ', ' * ', ' * ', ' * ']
        csv_writer.writerow(up_flow)

        down_flow = [' * ', e_d['mac'], ' * ', ' * ', ' * ', ' * ', ' * ', ' * ', ' * ']
        csv_writer.writerow(down_flow)


if __name__ == '__main__':
    files = ['18-06-17' ]
    write_flowentryfiles()


    for e_f in files:
        print(e_f)
        execute_sim(1,'/Users/Arunan/Documents/PCAP-Transfer/under_process/%s.pcap' % e_f,'/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/of_activity_time_measure/executesim/flowentries.csv')

        read_vol_attributes_config = {
            'instance_out_file': os.path.join(cfg.INSTANCE_OUTPUT_DIR, '%s.csv' % e_f),
            'flow_info_file': cfg.FLOW_INFO_FILE,
            'device_info': cfg.DEVICE_DICT,
            'gateway': cfg.GATE_WAY,
            'flow_meter_rate_file': cfg.FLOW_METER_RATE_FILE,
            'flow_meter_count_file': cfg.FLOW_METER_COUNT_FILE,
            'attribute_info': cfg.BUFFER,
            'tcam_rules_gen_function': cfg.tcam_rules,
            'annotation_offset':cfg.annotation_offset,
            'annotation_files':cfg.annotation_files
        }
        read_volumetric_attributes(read_vol_attributes_config)

        # print (dict_rate)
