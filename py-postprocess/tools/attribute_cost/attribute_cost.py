import re


def get_cost(attribute_list):
    attribute_list = [x.lower() for x in attribute_list]

    current_flows = []
    buffer_cost = 0

    cost_list = []

    for i in range(len(attribute_list)):

        m = re.search('^(\d+)min(\w+)(rate|count)', attribute_list[i])

        if m is not None:
            buffer_cost = buffer_cost + int(m.group(1))
            if m.group(2) not in current_flows:
                current_flows.append(m.group(2))
            # print([m.group(0),m.group(1),m.group(2)])
            cost_list.append([i, buffer_cost, len(current_flows)])
        else:
            raise ValueError('Reg Ex exception')

    return cost_list

if __name__=="__main__":
    selected_att_names = ['32minDNSDownCount', '64minDNSDownCount', '16minDNSDownRate', '64minDNSDownRate', '8minDNSUpRate', '16minDNSUpRate', '32minDNSUpRate', '64minDNSUpRate', '64minNTPDownRate', '32minNTPUpRate', '64minNTPUpRate', '4minLANDownRate', '4minANYWANDownCount', '8minANYWANDownCount', '16minANYWANDownCount', '32minANYWANDownCount', '64minANYWANDownCount', '1minANYWANDownRate', '64minANYWANDownRate', '1minANYWANUPCount', '2minANYWANUPCount', '4minANYWANUPCount', '32minANYWANUPCount', '1minANYWANUPRate', '2minANYWANUPRate', '8minANYWANUPRate', '64minANYWANUPRate', '64minSSDPUpCount', '4minSSDPUpRate', '8minSSDPUpRate', '64minSSDPUpRate']

    cost = get_cost(selected_att_names)
    for e in cost:
         print('%d\t%d\t%d'%(e[0],e[1],e[2]))