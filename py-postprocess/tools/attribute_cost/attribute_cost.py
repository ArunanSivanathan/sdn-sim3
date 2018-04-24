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
    selected_att_names = ['8minANYWANUpRate', '64minDNSUpRate', '1minANYWANUpRate', '64minANYWANDownRate',
                                  '32minDNSUpRate', '32minANYWANDownCount', '4minANYWANDownCount', '2minANYWANUpCount',
                                  '16minDNSUpRate', '64minNTPDownCount', '64minSSDPUpCount', '16minLANDownRate']

    cost = get_cost(selected_att_names)
    for e in cost:
         print('%d\t%d\t%d'%(e[0],e[1],e[2]))