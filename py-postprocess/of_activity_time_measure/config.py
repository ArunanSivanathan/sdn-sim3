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

annotation_offset = {
    '1':{'boot':[35,105], 'active':[-60,0]},
    '6':{'boot':[50,60], 'active':[-60,0]},
    '9':{'boot':[20,50], 'active':[-60,0]},
    '14':{'boot':[10,50], 'active':[-60,0]},
}

GATE_WAY = '14:cc:20:51:33:ea'

BUFFER = OrderedDict([('UpTraffic', {'length': 1 , 'src': 'rate', 'flow_col_name': 'UpTraffic'}),
                      ('DownTraffic', {'length': 1 , 'src': 'rate', 'flow_col_name': 'DownTraffic'})])


def tcam_rules(device_mac, gate_way_mac):
    tcam = {
        'UpTraffic': {'eth.src': device_mac},
        'DownTraffic': {'eth.dst': device_mac},
    }
    return tcam
