import csv
from operator import itemgetter

from statistics import mode
from matplotlib import pyplot


def extract_cols(file,cols):
    fid = open(file,'r')
    spam_reader = csv.reader(fid)

    output_rows = []
    col_keys = None
    l_seek =0
    for e_line in spam_reader:
        l_seek = l_seek + 1
        if l_seek==1:
            col_keys = itemgetter(*cols)(e_line)
            continue

        output_rows.append(itemgetter(*cols)(e_line))

    output_cols = list(map(list, zip(*output_rows)))

    for id_key in range(len(output_cols)):
        output_cols[id_key] =  list(map(int, output_cols[id_key]))

    fid.close()
    return output_cols,col_keys

def get_rows_by_value(data_list,col_index,value):
    output_list = []
    for i_cols in range(len(data_list)):
        output_list.append([])

    for i_row in range(len(data_list[0])):
        if data_list[col_index][i_row]==value:
            for i_cols in range(len(data_list)):
                output_list[i_cols].append(data_list[i_cols][i_row])

    return output_list

def draw_histogram(values,bins=None,alpha=None):
    n, bins, patches= pyplot.hist(values,bins,alpha=alpha)
    print (patches)
    pyplot.show()

if __name__=="__main__":
    bin_size=1024

    training_data, training_colkeys = extract_cols('../merge_instances/training.csv', [95, -1])
    training_filtered_row = get_rows_by_value(training_data, -1, 1)
    training_attribute_values = training_filtered_row[0]

    print('Attribute min:%d' % min(training_attribute_values))
    print('Attribute max:%d' % max(training_attribute_values))
    print('Attribute mode:%d' % mode(training_attribute_values))
    print('Bin size:%dBytes'%bin_size)
    print('X Limit:%dBytes'%xlimit)

    bins = range(min(training_attribute_values), max(training_attribute_values), bin_size)
    draw_histogram(training_filtered_row, bins)
    # print(filtered_rows)

    # fid = open('testing-Amazon_Echo_%s.csv'%keys[0],'w')
    # spam_writer  = csv.writer(fid)
    #
    # for each in filtered_rows[0]:
    #     spam_writer.writerow([each])
    #
    # fid.close()