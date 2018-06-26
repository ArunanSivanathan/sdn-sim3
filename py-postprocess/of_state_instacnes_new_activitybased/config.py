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
    {'mac': '70:ee:50:18:34:43', 'class': '17', 'name': 'Netatmo Camera'},
    {'mac': '00:16:6c:ab:6b:88', 'class': '21', 'name': 'Samsung Smart Camera'},
]

INSTANCE_INTERVAL = 1

GATE_WAY = '14:cc:20:51:33:ea'

BUFFER = OrderedDict([('1minDNSDown', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),
                      ('2minDNSDown', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),
                      ('4minDNSDown', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),

                      ('1minDNSUp', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),
                      ('2minDNSUp', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),
                      ('4minDNSUp', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),

                      ('1minNTPDown', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),
                      ('2minNTPDown', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),
                      ('4minNTPDown', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),

                      ('1minNTPUp', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),
                      ('2minNTPUp', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),
                      ('4minNTPUp', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),

                      ('1minDNSDownRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),
                      ('2minDNSDownRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),
                      ('4minDNSDownRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),

                      ('1minDNSUpRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),
                      ('2minDNSUpRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),
                      ('4minDNSUpRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),

                      ('1minNTPDownRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),
                      ('2minNTPDownRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),
                      ('4minNTPDownRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),

                      ('1minNTPUpRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),
                      ('2minNTPUpRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),
                      ('4minNTPUpRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),

                      ('1minLANDown', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),
                      ('2minLANDown', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),
                      ('4minLANDown', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),

                      ('1minLANDownRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),
                      ('2minLANDownRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),
                      ('4minLANDownRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),

                      ('1minANYWANDown', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),
                      ('2minANYWANDown', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),
                      ('4minANYWANDown', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),

                      ('1minANYWANDownRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),
                      ('2minANYWANDownRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),
                      ('4minANYWANDownRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),

                      ('1minANYWANUP', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),
                      ('2minANYWANUP', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),
                      ('4minANYWANUP', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),

                      ('1minANYWANUPRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),
                      ('2minANYWANUPRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),
                      ('4minANYWANUPRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),

                      ('1minSSDPUp', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),
                      ('2minSSDPUp', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),
                      ('4minSSDPUp', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),

                      ('1minSSDPUpRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),
                      ('2minSSDPUpRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),
                      ('4minSSDPUpRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),

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
