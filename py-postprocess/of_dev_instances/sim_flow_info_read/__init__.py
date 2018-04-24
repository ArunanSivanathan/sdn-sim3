import csv


class FlowInfoException(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class FlowInfoReader:
    def __init__(self, file_info):
        self.m_file_info = file_info
        self.m_flow_hash = self.load_flow_info()

    def load_flow_info(self):
        fid = open(self.m_file_info)
        spamreader = csv.reader(fid)

        flow_info_hash = {"eth.src": {}, "eth.dst": {}, "ip.src": {}, "ip.dst": {}, "ip.proto": {}, "port.src": {},
                          "port.dst": {}}

        line = 0
        for csv_line in spamreader:
            line = line + 1
            if line == 1:
                continue

            flow_id = int(csv_line[0])
            eth_src = csv_line[1].lower()
            eth_dst = csv_line[2].lower()
            ip_src = csv_line[3]
            ip_dst = csv_line[4]
            ip_proto = csv_line[5]
            port_src = csv_line[6]
            port_dst = csv_line[7]

            if eth_src not in flow_info_hash["eth.src"]:
                flow_info_hash["eth.src"][eth_src] = set()
            flow_info_hash["eth.src"][eth_src].add(flow_id)

            if eth_dst not in flow_info_hash["eth.dst"]:
                flow_info_hash["eth.dst"][eth_dst] = set()
            flow_info_hash["eth.dst"][eth_dst].add(flow_id)

            if ip_src not in flow_info_hash["ip.src"]:
                flow_info_hash["ip.src"][ip_src] = set()
            flow_info_hash["ip.src"][ip_src].add(flow_id)

            if ip_dst not in flow_info_hash["ip.dst"]:
                flow_info_hash["ip.dst"][ip_dst] = set()
            flow_info_hash["ip.dst"][ip_dst].add(flow_id)

            if ip_proto not in flow_info_hash["ip.proto"]:
                flow_info_hash["ip.proto"][ip_proto] = set()
            flow_info_hash["ip.proto"][ip_proto].add(flow_id)

            if port_src not in flow_info_hash["port.src"]:
                flow_info_hash["port.src"][port_src] = set()
            flow_info_hash["port.src"][port_src].add(flow_id)

            if port_dst not in flow_info_hash["port.dst"]:
                flow_info_hash["port.dst"][port_dst] = set()
            flow_info_hash["port.dst"][port_dst].add(flow_id)

        fid.close()

        return flow_info_hash

    def find_flow_ids(self, flow_match):
        match_flows = None
        for e_field in self.m_flow_hash:
            if e_field in flow_match:
                if match_flows is None:
                    match_flows = self.m_flow_hash[e_field][flow_match[e_field]]
                else:
                    match_flows = match_flows.intersection(self.m_flow_hash[e_field][flow_match[e_field]])
            # Todo: select high priority

        return match_flows

    def find_device_flows(self, rule_dict):
        device_flows = {}
        for e_rule_name in rule_dict:
            rule_id = self.find_flow_ids(rule_dict[e_rule_name])
            if len(rule_id) > 1:
                raise (FlowInfoException("More than one ID found for {}".format(e_rule_name)))
            elif len(rule_id) == 0:
                raise (FlowInfoException("No ID found for {}".format(e_rule_name)))
            device_flows[e_rule_name] = next(iter(rule_id))#select 1st element in the set

        return device_flows
