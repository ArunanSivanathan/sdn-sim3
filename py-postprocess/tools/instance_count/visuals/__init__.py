import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cbook
from matplotlib.collections import PatchCollection

import numpy

total_people = 0
font = {"fontname": "serif", "weight": "regular"}
titlefont = {'fontsize': 14, "weight": "semibold"}

def absolute_value(val):
    num = numpy.round(val / 100. * total_people, 0)
    if val == 0:
        return ''
    else:
        return '%d/%d\n(%0.1f%%)' % (num, total_people, val)


def drawpie(sizes, labels, colors, title, groups,explode,filename='',legend_loc='upper right',legend_cols=1):
    global total_people
    total_people = sum(sizes)

    f = plt.figure( figsize=(7, 9), dpi=80, facecolor='w', edgecolor='k')
    # ax = f.add_axes((0, 0, 1, 1))

    handle = plt.pie(sizes, colors=colors,
                     autopct=absolute_value,
                     startangle=140,
                     textprops=font,
                     wedgeprops={"edgecolor":"k",'linewidth': 0.4, 'linestyle': 'solid', 'antialiased': True},
                     pctdistance=0.7,
                     shadow=True)
    plt.legend(handle, labels=labels, loc=legend_loc,ncol=legend_cols)
    # plt.legend(handle,loc="bottom",  borderaxespad=0.)
    # plt.legend(handle, labels=labels, bbox_to_anchor=(1,0),bbox_transform=plt.gcf().transFigure)
    # plt.subplots_adjust(left=0.0, top=0.95)

    plt.title(title,fontdict=titlefont)
    ax = plt.gca()
    ttl = ax.title
    # ttl.set_position([.5, 1.08])



    wedges = handle[0]
    percentage_txt = handle[2]

    plt.axis('equal')
    plt.tight_layout()


    for grped_wedge_ids, exp in cbook.safezip(groups,explode):
        ang = numpy.deg2rad((wedges[grped_wedge_ids[-1]].theta2 + wedges[grped_wedge_ids[0]].theta1) / 2, )
        for each_wedge_id in grped_wedge_ids:
            we = wedges[each_wedge_id]
            center = (exp * we.r * numpy.cos(ang), exp * we.r * numpy.sin(ang))
            #if it a small wedge
            small_offset=[0,0]
            if (we.theta2-we.theta1)<6:
                we_angle= numpy.deg2rad((we.theta2 + we.theta1) / 2, )
                small_offset=(0.4 * we.r * numpy.cos(we_angle), 0.4* we.r * numpy.sin(we_angle))
            percentage_txt[each_wedge_id]._x = center[0]+percentage_txt[each_wedge_id]._x+small_offset[0]
            percentage_txt[each_wedge_id]._y = center[1]+percentage_txt[each_wedge_id]._y+small_offset[1]
            we.set_center(center)

    f.savefig(('./images/%s %s.png'%(filename,title)))
    plt.show()


def draw_stackbar(data_dict,bar_colors,tick_labels,color_labels,title,tick_rotation='vertical',legend_cols=1,filename='',ylabel = 'Number of people'):
    f = plt.figure( figsize=(7, 7), dpi=80, facecolor='w', edgecolor='k')
    N = len(tick_labels)

    ind = range(N)  # the x locations for the groups
    width = 0.25  # the width of the bars: can also be len(x) sequence

    last_level = [0]*N

    for layer_id in  range(len(data_dict)):
        layer_name = color_labels[layer_id]
        p1 = plt.bar(ind, data_dict[layer_name],color=bar_colors[layer_id],bottom=last_level)

        for i in range(N):
            last_level[i]+=data_dict[layer_name][i]

        print (last_level)



    plt.ylabel(ylabel)

    plt.title(title,fontdict=titlefont)
    ax = plt.gca()
    ttl = ax.title
    ttl.set_position([.5, 1.08])
    plt.xticks(ind,tick_labels,rotation=tick_rotation,multialignment="right")
    # plt.xticks(rotation=70)
    if last_level[0]<10:
        y_gap=1
    elif last_level[0] == 1:
        y_gap = 0.5
    else:
        y_gap=10
    plt.ylim([0,last_level[0]])
    ticks = numpy.arange(0, last_level[0]+1, y_gap)
    plt.yticks(ticks)

    plt.legend(color_labels,ncol=legend_cols,bbox_to_anchor=(-0.15, 1.02, 1., .102),  borderaxespad=0.,loc=3)
    plt.gcf().subplots_adjust(bottom=0.35)
    f.savefig(('./images/%s%s.png'%(filename,title)))

def draw_bar(data_dict,  tick_labels, bar_colors=None ,color_labels=None, title=None, tick_rotation='vertical', legend_cols=1,
                      filename='', ylabel='Number of people'):
        f = plt.figure(figsize=(7, 7), dpi=80, facecolor='w', edgecolor='k')
        N = len(tick_labels)

        ind = range(N)  # the x locations for the groups
        width = 1  # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind,data_dict.values())
        plt.ylabel(ylabel)
        if title is not None:
            plt.title(title, fontdict=titlefont)
        ax = plt.gca()
        ttl = ax.title

        plt.xticks(ind, tick_labels, rotation=tick_rotation, multialignment="right")
        # plt.xticks(rotation=70)

        max_ytick = max(data_dict.values())
        y_gap = 1000
        plt.ylim([0, max_ytick])
        ticks = numpy.arange(0, max_ytick + 1, y_gap)
        plt.yticks(ticks)


        if filename is not None:
            f.savefig(filename)


def showfigure():
    plt.show()
