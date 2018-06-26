import os
import re


def list_files(basepath):
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(basepath) for f in filenames]

def dict_files(basepath):
    dict_files={}
    for dp, dn, filenames in os.walk(basepath):
        for f in filenames:
            x = dict_files.get(dp, list())
            x.append(f)
            dict_files[dp] =  x

    return dict_files
# def filter_files(regEx,file_list):
#     filtered_list =[]
#     for e in file_list:
#         m = re.search(regEx, e)
#         if m is not None:
#             filtered_list.append(e)
#     return filtered_list

if __name__ =='__main__':
    filenames =  list_files('/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/tools/split_state_instance_devices/csv_files/')
    # filtered_list = filter_files(r"*\.pcap",filenames)

    [print(fn) for fn in filenames]
    # file_dict = dict_files('/Volumes/Seagate Backup Plus Drive/states-last-franco')
    # print(file_dict.keys())