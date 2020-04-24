# SDN Switch Emulator V3

``usage: sdn_sim3 [options] <pcap_path> [<controller_id>] [-- <controller_options...>]
options:
 --verbose	verbose output
 --brief	brief output
 -r, --resolution=<T>	Logging resolution in Secs[default:60]


Controllers:
 ofdc			Openflow device classification
 simplestatic	Simple static flows
 dnsparser	Parse DNS packets


sdn_sim3 --verbose -r 60 -o ../data/ ap_packets.pcap simplestatic -- --flowentries ../data/tcam_rules.csv