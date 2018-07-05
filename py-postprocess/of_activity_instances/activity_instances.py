import os
from of_activity_instances.executesim import execute_sim
import of_activity_instances.config as cfg
import of_activity_instances.sim_flow_info_read as f_info
import of_activity_instances.sim_flow_meter_read as f_meter
from of_activity_instances.of_volumetric_attribute_writer import OFVolumetricAttributeWriter
import of_activity_instances.annotate_states as a_s


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
    state_annotator = a_s.AnnotateStates(annotation_files,annotation_offset,cfg.SIM_RESOLUTION)

    for e_device in device_info:
        print(e_device['class'])

        dev_flows = flow_info.find_device_flows(tcam_rules_gen_function(e_device['mac'], gateway_mac))
        attribute_writer.flow_info_dict = dev_flows

        flow_meter = f_meter.FlowMeterReader(flow_meter_rate_file, flow_meter_count_file)

        for tid, dict_rate, dict_count in flow_meter:
            labels = [e_device['class'],state_annotator.annotate(e_device['class'],tid)]
            attribute_writer.put_reading(tid, dict_rate, dict_count,labels)


if __name__ == '__main__':
    files = ['18-06-14','18-06-26']

    # files = [
    #     '18-02-14', '18-02-15', '18-02-16', '18-02-17', '18-02-18', '18-02-19', '18-02-20', '18-02-21', '18-02-22',
    #     '18-02-23', '18-02-24', '18-02-25', '18-02-26', '18-02-27', '18-02-28', '18-03-01', '18-03-02', '18-03-03',
    #     '18-03-04', '18-03-05', '18-03-06', '18-03-07', '18-03-08', '18-03-09', '18-03-10', '18-03-11' ]

    for e_f in files:
        print(e_f)
        execute_sim(cfg.SIM_RESOLUTION,'/Users/Arunan/Documents/PCAP-Transfer/under_process/activity/%s.pcap' % e_f)

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
