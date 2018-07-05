from collections import OrderedDict

DATA_DIR = '../../cmake-build-debug/'
INSTANCE_OUTPUT_DIR = './instances'

FLOW_INFO_FILE = '{}/{}'.format(DATA_DIR, 'log_flowentries.csv')
FLOW_METER_RATE_FILE = '{}/{}'.format(DATA_DIR, 'log_flowusage_data.csv')
FLOW_METER_COUNT_FILE = '{}/{}'.format(DATA_DIR, 'log_flowusage_packet.csv')
DEVICE_DICT = [
    {'mac': '44:65:0d:56:cc:d3', 'class': '1', 'name': 'Amazon Echo'},
    {'mac': 'ec:1a:59:79:f4:89', 'class': '6', 'name': 'Belkin Switch'},
    {'mac': 'ec:1a:59:7a:02:c5', 'class': '6', 'name': 'Belkin Switch'},
    {'mac': '30:8c:fb:2f:e4:b2', 'class': '9', 'name': 'Dropcam'},
    {'mac': '30:8c:fb:b6:ea:45', 'class': '9', 'name': 'Dropcam'},
    {'mac': '30:8c:fb:2f:57:d7', 'class': '9', 'name': 'Dropcam'},
    {'mac': 'd0:73:d5:01:83:08', 'class': '14', 'name': 'LiFX Bulb'},
]

annotation_files = ['/Users/Arunan/Documents/PCAP-Transfer/under_process/activity/boot_annotation.txt', '/Users/Arunan/Documents/PCAP-Transfer/under_process/activity/activity_annotation.txt']

# annotation_offset = {
#     '1':{'boot':[35,105], 'active':[-60,0]},
#     '6':{'boot':[50,60], 'active':[-60,0]},
#     '9':{'boot':[20,50], 'active':[-60,0]},
#     '14':{'boot':[10,50], 'active':[-60,0]},
# }

annotation_offset = {
    '1':{'boot':[35,105], 'active':[-60+10,-45+10]},
    '6':{'boot':[50,60], 'active':[-85+10,-60+10]},
    '9':{'boot':[20,50], 'active':[-70+10,-30+10]},
    '14':{'boot':[10,50], 'active':[-55+10,-30+10]},
}

SIM_RESOLUTION = 60

GATE_WAY = '14:cc:20:51:33:ea'

minute_conversion = 60.0/float(SIM_RESOLUTION)

'''
Safty check
'''
attribute_time_ranges = [1 * minute_conversion, 2 * minute_conversion,4 * minute_conversion]
buffer_name_size={'1':{'name':'1min','buffer':int(1 * minute_conversion)},
                  '2': {'name': '2min', 'buffer': int(2 * minute_conversion)},
                  '4': {'name': '4min', 'buffer': int(4 * minute_conversion)},}

for e_a in buffer_name_size:
    if int(buffer_name_size[e_a]['buffer']) <= 0:
        raise ("Cannot generate %d buffer from %d resolution"%(buffer_name_size[e_a]['buffer'],SIM_RESOLUTION))

BUFFER = OrderedDict([('1minDNSDownCount', {'length': buffer_name_size['1']['buffer'], 'src': 'count', 'flow_col_name': 'mac2dns-down'}),
                      ('2minDNSDownCount', {'length': buffer_name_size['2']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),
                      ('4minDNSDownCount', {'length': buffer_name_size['4']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),

                      ('1minDNSUpCount', {'length': buffer_name_size['1']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),
                      ('2minDNSUpCount', {'length': buffer_name_size['2']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),
                      ('4minDNSUpCount', {'length': buffer_name_size['4']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),

                      ('1minNTPDownCount', {'length': buffer_name_size['1']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),
                      ('2minNTPDownCount', {'length': buffer_name_size['2']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),
                      ('4minNTPDownCount', {'length': buffer_name_size['4']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),

                      ('1minNTPUpCount', {'length': buffer_name_size['1']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),
                      ('2minNTPUpCount', {'length': buffer_name_size['2']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),
                      ('4minNTPUpCount', {'length': buffer_name_size['4']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),

                      ('1minDNSDownRate', {'length': buffer_name_size['1']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),
                      ('2minDNSDownRate', {'length': buffer_name_size['2']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),
                      ('4minDNSDownRate', {'length': buffer_name_size['4']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),

                      ('1minDNSUpRate', {'length': buffer_name_size['1']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),
                      ('2minDNSUpRate', {'length': buffer_name_size['2']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),
                      ('4minDNSUpRate', {'length': buffer_name_size['4']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),

                      ('1minNTPDownRate', {'length': buffer_name_size['1']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),
                      ('2minNTPDownRate', {'length': buffer_name_size['2']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),
                      ('4minNTPDownRate', {'length': buffer_name_size['4']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),

                      ('1minNTPUpRate', {'length': buffer_name_size['1']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),
                      ('2minNTPUpRate', {'length': buffer_name_size['2']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),
                      ('4minNTPUpRate', {'length': buffer_name_size['4']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),

                      ('1minLANDownCount', {'length': buffer_name_size['1']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),
                      ('2minLANDownCount', {'length': buffer_name_size['2']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),
                      ('4minLANDownCount', {'length': buffer_name_size['4']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),

                      ('1minLANDownRate', {'length': buffer_name_size['1']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),
                      ('2minLANDownRate', {'length': buffer_name_size['2']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),
                      ('4minLANDownRate', {'length': buffer_name_size['4']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),

                      ('1minANYWANDownCount', {'length': buffer_name_size['1']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),
                      ('2minANYWANDownCount', {'length': buffer_name_size['2']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),
                      ('4minANYWANDownCount', {'length': buffer_name_size['4']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),

                      ('1minANYWANDownRate', {'length': buffer_name_size['1']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),
                      ('2minANYWANDownRate', {'length': buffer_name_size['2']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),
                      ('4minANYWANDownRate', {'length': buffer_name_size['4']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),

                      ('1minANYWANUpCount', {'length': buffer_name_size['1']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),
                      ('2minANYWANUpCount', {'length': buffer_name_size['2']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),
                      ('4minANYWANUpCount', {'length': buffer_name_size['4']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),

                      ('1minANYWANUpRate', {'length': buffer_name_size['1']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),
                      ('2minANYWANUpRate', {'length': buffer_name_size['2']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),
                      ('4minANYWANUpRate', {'length': buffer_name_size['4']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),

                      ('1minSSDPUpCount', {'length': buffer_name_size['1']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),
                      ('2minSSDPUpCount', {'length': buffer_name_size['2']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),
                      ('4minSSDPUpCount', {'length': buffer_name_size['4']['buffer'] , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),

                      ('1minSSDPUpRate', {'length': buffer_name_size['1']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),
                      ('2minSSDPUpRate', {'length': buffer_name_size['2']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),
                      ('4minSSDPUpRate', {'length': buffer_name_size['4']['buffer'] , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),

                      ])


def tcam_rules(device_mac, gate_way_mac):
    tcam = {
        'mac2dns-up': {'eth.src': device_mac, 'eth.dst': gate_way_mac, 'port.src': '0', 'port.dst': '53',
                       'IP.proto': '0x0'},
        'mac2dns-down': {'eth.src': gate_way_mac, 'eth.dst': device_mac, 'port.src': '53', 'port.dst': '0',
                         'IP.proto': '0x0'},

        'mac2ntp-up': {'eth.src': device_mac, 'eth.dst': gate_way_mac, 'port.src': '0', 'port.dst': '123',
                       'IP.proto': '0x0'},
        'mac2ntp-down': {'eth.src': gate_way_mac, 'eth.dst': device_mac, 'port.src': '123', 'port.dst': '0',
                         'IP.proto': '0x0'},

        'mac2ssdp-up': {'eth.src': device_mac, 'port.src': '0', 'port.dst': '1900',
                        'IP.proto': '0x0'},

        'mac2anywan-up': {'eth.src': device_mac, 'eth.dst': gate_way_mac, 'port.src': '0', 'port.dst': '0',
                          'IP.proto': '0x0'},
        'mac2anywan-down': {'eth.src': gate_way_mac, 'eth.dst': device_mac, 'port.src': '0', 'port.dst': '0',
                            'IP.proto': '0x0'},

        'mac2anylan-down': {'eth.src': '', 'eth.dst': device_mac, 'port.src': '0', 'port.dst': '0',
                            'IP.proto': '0x0'}
    }
    return tcam
