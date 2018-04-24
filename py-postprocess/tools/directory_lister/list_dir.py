import os
import re


def list_files(basepath):
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(basepath) for f in filenames]

# def filter_files(regEx,file_list):
#     filtered_list =[]
#     for e in file_list:
#         m = re.search(regEx, e)
#         if m is not None:
#             filtered_list.append(e)
#     return filtered_list

if __name__ =='__main__':
    filenames =  list_files('/Volumes/Seagate Backup Plus Drive/Ayyoob/pcap/training/24hour/')
    # filtered_list = filter_files(r"*\.pcap",filenames)

    [print(fn) for fn in filenames]