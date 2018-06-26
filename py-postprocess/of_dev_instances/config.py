from collections import OrderedDict

DATA_DIR = '../../cmake-build-debug/'
INSTANCE_OUTPUT_DIR = './instances'

FLOW_INFO_FILE = '{}/{}'.format(DATA_DIR, 'log_flowentries.csv')
FLOW_METER_RATE_FILE = '{}/{}'.format(DATA_DIR, 'log_flowusage_data.csv')
FLOW_METER_COUNT_FILE = '{}/{}'.format(DATA_DIR, 'log_flowusage_packet.csv')
DEVICE_DICT = [
    {'mac': '44:65:0d:56:cc:d3', 'class': '1', 'name': 'Amazon Echo'},
    {'mac': 'e0:76:d0:3f:00:ae', 'class': '2', 'name': 'August Doorbell '},
    {'mac': '70:88:6b:10:0f:c6', 'class': '3', 'name': 'Awair air quality'},
    {'mac': 'ec:1a:59:83:28:11', 'class': '5', 'name': 'Belkin Motion Sensor'},
    {'mac': 'ec:1a:59:79:50:1d', 'class': '5', 'name': 'Belkin Motion Sensor'},
    {'mac': 'ec:1a:59:79:f4:89', 'class': '6', 'name': 'Belkin Switch'},
    {'mac': 'ec:1a:59:7a:02:c5', 'class': '6', 'name': 'Belkin Switch'},
    {'mac': '30:8c:fb:2f:e4:b2', 'class': '9', 'name': 'Dropcam'},
    {'mac': '30:8c:fb:b6:ea:45', 'class': '9', 'name': 'Dropcam'},
    {'mac': '30:8c:fb:2f:57:d7', 'class': '9', 'name': 'Dropcam'},
    {'mac': '70:5a:0f:e4:9b:c0', 'class': '12', 'name': 'HP Printer'},
    {'mac': 'd0:73:d5:01:83:08', 'class': '14', 'name': 'LiFX Bulb'},
    {'mac': '18:b4:30:25:be:e4', 'class': '15', 'name': 'NEST Smoke Sensor'},
    {'mac': '70:ee:50:03:b8:ac', 'class': '16', 'name': 'Netatmo Weather'},
    {'mac': '70:ee:50:18:34:43', 'class': '17', 'name': 'Netatmo Camera'},
    {'mac': '00:17:88:2b:9a:25', 'class': '18', 'name': 'Hue Bulb'},
    {'mac': '00:16:6c:ab:6b:88', 'class': '21', 'name': 'Samsung Smart Camera'},
    {'mac': 'd0:52:a8:00:67:5e', 'class': '22', 'name': 'Smart Things'},
    {'mac': 'd0:52:a8:00:68:08', 'class': '22', 'name': 'Smart Things'},
    {'mac': '18:b7:9e:02:20:44', 'class': '25', 'name': 'Triby Speaker'},
    {'mac': '00:24:e4:20:28:c6', 'class': '26', 'name': 'Withings sleep sensor'},
    {'mac': '00:24:e4:44:68:44', 'class': '28', 'name': 'Withings Scale'},
    {'mac': '00:24:e4:1b:6f:96', 'class': '28', 'name': 'Withings Scale'},
    {'mac': '00:24:e4:11:57:d7', 'class': '28', 'name': 'Withings Scale'},
    {'mac': '40:f3:08:ff:1e:da', 'class': '99', 'name': 'Non IoT'},
    {'mac': '74:2f:68:81:69:42', 'class': '99', 'name': 'Non IoT'},
    {'mac': 'ac:bc:32:d4:6f:2f', 'class': '99', 'name': 'Non IoT'},
    {'mac': 'b4:ce:f6:a7:a3:c2', 'class': '99', 'name': 'Non IoT'},
    {'mac': 'd0:a6:37:df:a1:e1', 'class': '99', 'name': 'Non IoT'},
    {'mac': 'f4:5c:89:93:cc:85', 'class': '99', 'name': 'Non IoT'},
]

INSTANCE_INTERVAL = 15

GATE_WAY = '14:cc:20:51:33:ea'

BUFFER = OrderedDict([('1minDNSDown', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),
                      ('2minDNSDown', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),
                      ('4minDNSDown', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),
                      ('8minDNSDown', {'length': 8 , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),
                      ('16minDNSDown', {'length': 16 , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),
                      ('32minDNSDown', {'length': 32 , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),
                      ('64minDNSDown', {'length': 64 , 'src': 'count', 'flow_col_name': 'mac2dns-down'}),

                      ('1minDNSUp', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),
                      ('2minDNSUp', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),
                      ('4minDNSUp', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),
                      ('8minDNSUp', {'length': 8 , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),
                      ('16minDNSUp', {'length': 16 , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),
                      ('32minDNSUp', {'length': 32 , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),
                      ('64minDNSUp', {'length': 64 , 'src': 'count', 'flow_col_name': 'mac2dns-up'}),

                      ('1minNTPDown', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),
                      ('2minNTPDown', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),
                      ('4minNTPDown', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),
                      ('8minNTPDown', {'length': 8 , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),
                      ('16minNTPDown', {'length': 16 , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),
                      ('32minNTPDown', {'length': 32 , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),
                      ('64minNTPDown', {'length': 64 , 'src': 'count', 'flow_col_name': 'mac2ntp-down'}),

                      ('1minNTPUp', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),
                      ('2minNTPUp', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),
                      ('4minNTPUp', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),
                      ('8minNTPUp', {'length': 8 , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),
                      ('16minNTPUp', {'length': 16 , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),
                      ('32minNTPUp', {'length': 32 , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),
                      ('64minNTPUp', {'length': 64 , 'src': 'count', 'flow_col_name': 'mac2ntp-up'}),

                      ('1minDNSDownRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),
                      ('2minDNSDownRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),
                      ('4minDNSDownRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),
                      ('8minDNSDownRate', {'length': 8 , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),
                      ('16minDNSDownRate', {'length': 16 , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),
                      ('32minDNSDownRate', {'length': 32 , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),
                      ('64minDNSDownRate', {'length': 64 , 'src': 'rate', 'flow_col_name': 'mac2dns-down'}),

                      ('1minDNSUpRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),
                      ('2minDNSUpRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),
                      ('4minDNSUpRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),
                      ('8minDNSUpRate', {'length': 8 , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),
                      ('16minDNSUpRate', {'length': 16 , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),
                      ('32minDNSUpRate', {'length': 32 , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),
                      ('64minDNSUpRate', {'length': 64 , 'src': 'rate', 'flow_col_name': 'mac2dns-up'}),

                      ('1minNTPDownRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),
                      ('2minNTPDownRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),
                      ('4minNTPDownRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),
                      ('8minNTPDownRate', {'length': 8 , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),
                      ('16minNTPDownRate', {'length': 16 , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),
                      ('32minNTPDownRate', {'length': 32 , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),
                      ('64minNTPDownRate', {'length': 64 , 'src': 'rate', 'flow_col_name': 'mac2ntp-down'}),

                      ('1minNTPUpRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),
                      ('2minNTPUpRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),
                      ('4minNTPUpRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),
                      ('8minNTPUpRate', {'length': 8 , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),
                      ('16minNTPUpRate', {'length': 16 , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),
                      ('32minNTPUpRate', {'length': 32 , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),
                      ('64minNTPUpRate', {'length': 64 , 'src': 'rate', 'flow_col_name': 'mac2ntp-up'}),

                      ('1minLANDown', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),
                      ('2minLANDown', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),
                      ('4minLANDown', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),
                      ('8minLANDown', {'length': 8 , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),
                      ('16minLANDown', {'length': 16 , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),
                      ('32minLANDown', {'length': 32 , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),
                      ('64minLANDown', {'length': 64 , 'src': 'count', 'flow_col_name': 'mac2anylan-down'}),

                      ('1minLANDownRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),
                      ('2minLANDownRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),
                      ('4minLANDownRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),
                      ('8minLANDownRate', {'length': 8 , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),
                      ('16minLANDownRate', {'length': 16 , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),
                      ('32minLANDownRate', {'length': 32 , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),
                      ('64minLANDownRate', {'length': 64 , 'src': 'rate', 'flow_col_name': 'mac2anylan-down'}),

                      ('1minANYWANDown', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),
                      ('2minANYWANDown', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),
                      ('4minANYWANDown', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),
                      ('8minANYWANDown', {'length': 8 , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),
                      ('16minANYWANDown', {'length': 16 , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),
                      ('32minANYWANDown', {'length': 32 , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),
                      ('64minANYWANDown', {'length': 64 , 'src': 'count', 'flow_col_name': 'mac2anywan-down'}),

                      ('1minANYWANDownRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),
                      ('2minANYWANDownRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),
                      ('4minANYWANDownRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),
                      ('8minANYWANDownRate', {'length': 8 , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),
                      ('16minANYWANDownRate', {'length': 16 , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),
                      ('32minANYWANDownRate', {'length': 32 , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),
                      ('64minANYWANDownRate', {'length': 64 , 'src': 'rate', 'flow_col_name': 'mac2anywan-down'}),

                      ('1minANYWANUP', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),
                      ('2minANYWANUP', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),
                      ('4minANYWANUP', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),
                      ('8minANYWANUP', {'length': 8 , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),
                      ('16minANYWANUP', {'length': 16 , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),
                      ('32minANYWANUP', {'length': 32 , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),
                      ('64minANYWANUP', {'length': 64 , 'src': 'count', 'flow_col_name': 'mac2anywan-up'}),

                      ('1minANYWANUPRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),
                      ('2minANYWANUPRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),
                      ('4minANYWANUPRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),
                      ('8minANYWANUPRate', {'length': 8 , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),
                      ('16minANYWANUPRate', {'length': 16 , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),
                      ('32minANYWANUPRate', {'length': 32 , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),
                      ('64minANYWANUPRate', {'length': 64 , 'src': 'rate', 'flow_col_name': 'mac2anywan-up'}),

                      ('1minSSDPUp', {'length': 1 , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),
                      ('2minSSDPUp', {'length': 2 , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),
                      ('4minSSDPUp', {'length': 4 , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),
                      ('8minSSDPUp', {'length': 8 , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),
                      ('16minSSDPUp', {'length': 16 , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),
                      ('32minSSDPUp', {'length': 32 , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),
                      ('64minSSDPUp', {'length': 64 , 'src': 'count', 'flow_col_name': 'mac2ssdp-up'}),

                      ('1minSSDPUpRate', {'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),
                      ('2minSSDPUpRate', {'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),
                      ('4minSSDPUpRate', {'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),
                      ('8minSSDPUpRate', {'length': 8 , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),
                      ('16minSSDPUpRate', {'length': 16 , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),
                      ('32minSSDPUpRate', {'length': 32 , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),
                      ('64minSSDPUpRate', {'length': 64 , 'src': 'rate', 'flow_col_name': 'mac2ssdp-up'}),

                      # ('1minSNMPUp',{ 'length': 1 , 'src': 'count', 'flow_col_name': 'mac2snmp-up'}),
                      # ('2minSNMPUp',{ 'length': 2 , 'src': 'count', 'flow_col_name': 'mac2snmp-up'}),
                      # ('4minSNMPUp',{ 'length': 4 , 'src': 'count', 'flow_col_name': 'mac2snmp-up'}),
                      # ('8minSNMPUp',{ 'length': 8 , 'src': 'count', 'flow_col_name': 'mac2snmp-up'}),
                      # ('16minSNMPUp',{ 'length': 16 , 'src': 'count', 'flow_col_name': 'mac2snmp-up'}),
                      # ('32minSNMPUp',{ 'length': 32 , 'src': 'count', 'flow_col_name': 'mac2snmp-up'}),
                      # ('64minSNMPUp', { 'length': 64 , 'src': 'count', 'flow_col_name': 'mac2snmp-up'}),
                      #
                      # ('1minSNMPUpRate',{ 'length': 1 , 'src': 'rate', 'flow_col_name': 'mac2snmp-up'}),
                      # ('2minSNMPUpRate',{ 'length': 2 , 'src': 'rate', 'flow_col_name': 'mac2snmp-up'}),
                      # ('4minSNMPUpRate',{ 'length': 4 , 'src': 'rate', 'flow_col_name': 'mac2snmp-up'}),
                      # ('8minSNMPUpRate',{ 'length': 8 , 'src': 'rate', 'flow_col_name': 'mac2snmp-up'}),
                      # ('16minSNMPUpRate',{ 'length': 16 , 'src': 'rate', 'flow_col_name': 'mac2snmp-up'}),
                      # ('32minSNMPUpRate',{ 'length': 32 , 'src': 'rate', 'flow_col_name': 'mac2snmp-up'}),
                      # ('64minSNMPUpRate', { 'length': 64 , 'src': 'rate', 'flow_col_name': 'mac2snmp-up'}),
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
