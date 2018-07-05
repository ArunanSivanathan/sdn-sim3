import csv
import matplotlib.pyplot as plt
from plotly.utils import numpy

import visuals


class InstanceCounter():
    def __init__(self, inputfile):
        self.input_file = inputfile
        self.instance_histogram={}

    def count_instance(self):
        fid = open(self.input_file)
        csv_reader = csv.reader(fid)
        self.instance_histogram = {}
        l_seek = 0
        for e_l in csv_reader:
            l_seek = l_seek+1
            if l_seek == 1:
                continue

            self.instance_histogram[e_l[-1]]= self.instance_histogram.get(e_l[-1],0) +1
        return self.instance_histogram


def plot_bar(bar_height, xticks,ylabel,yinterval = None,title=None,filename=None):
    font = {"fontname": "serif", "weight": "regular"}
    titlefont = {'fontsize': 14, "weight": "semibold"}

    f = plt.figure(figsize=(7, 7), dpi=80, facecolor='w', edgecolor='k')

    N = len(bar_height)
    ind = range(N)  # the x locations for the groups

    p1 = plt.bar(ind, bar_height,color='#ff0000')
    plt.ylabel(ylabel)
    if title is not None:
        plt.title(title, fontdict=titlefont)
    ax = plt.gca()
    ttl = ax.title

    plt.xticks(ind, xticks, rotation='vertical', multialignment="right")

    max_ytick = max(bar_height)
    if yinterval is None:
        yinterval = max_ytick/10.0


    plt.ylim([0, max_ytick + yinterval])
    ticks = numpy.arange(0, max_ytick + yinterval, yinterval)
    plt.yticks(ticks)


    plt.gcf().subplots_adjust(bottom=0.35)
    plt.gca().yaxis.grid(True)

    if filename is not None:
        f.savefig(filename)

    # plt.show()


def ordered_values(stat_dict, ordered_label,unequal_label=False):
    if not unequal_label and  len(stat_dict) > len(ordered_label):
        raise KeyError('number of stat_dict labels are greater than labels provided')

    vals = []
    for each_label in ordered_label:
        vals.append(stat_dict.get(each_label, 0))

    return vals

if __name__ == "__main__":
    csv_files = ['device_identification_full_dataset-training']

    for filename in csv_files:
        ic = InstanceCounter('../merge_instances/%s.csv' % filename)
        ic_value_dict = ic.count_instance()

        plot_order = ['1', '2', '3', '5', '6', '9', '12', '14', '15', '16', '17','18', '21', '22', '25', '26', '28','99']
        device_names = {'1':'Amazon Echo',
                        '2':'August Doorbell',
                        '3':'Awair air quality',
                        '5':'Belkin Motion Sensor',
                        '6':'Belkin Switch',
                        '9':'Dropcam',
                        '12':'HP Printer',
                        '14':'LiFX Bulb',
                        '15':'NEST Smoke Sensor',
                        '16':'Netatmo Weather',
                        '17':'Netatmo Camera',
                        '18':'Hue Bulb',
                        '21':'Samsung Smart Camera',
                        '22':'Smart Things',
                        '25':'Triby Speaker',
                        '26':'Withings sleep sensor',
                        '28':'Withings Scale',
                        '99': 'Non-IoT'}

        bar_heights = order_vals = ordered_values(ic_value_dict,plot_order)
        device_labels = ordered_values(device_names,device_names)
        plot_bar(bar_heights,device_labels,'Number of Instances',filename='./instance-count-%s.png'%filename)
        # visuals.draw_bar(ic.instance_histogram,ic.instance_histogram.keys(),ylabel='Number of Instances')
        # visuals.showfigure()
