import os
import subprocess

def simple_merge_pcap(input_folder, output_filename):
    print(" ".join(["mergecap", "-w", output_filename, input_folder]))
    os.system(" ".join(["mergecap", "-w", output_filename, input_folder]))

def merge_day_files(input_folder,output_filename): #Written by Ayyoob to merge wan,lan traffic of all flows

    simple_merge_pcap(input_folder,'%sx.pcap'%output_filename)
    command = "editcap -w 0.05 '%sx.pcap' '%s.pcap'" % (output_filename,output_filename)
    print(command)
    return_code = subprocess.call(command, shell=True)

    command = "rm '%sx.pcap'" % (output_filename)
    print(command)
    return_code = subprocess.call(command, shell=True)

if __name__ == "__main__":
    pcap_list = ['/Users/Arunan/Documents/PCAP-Transfer/under_process/18-06-17']

    for e_p in pcap_list:
        ep_without_space = e_p.replace(' ', '\ ')
        merge_day_files('%s/*' % ep_without_space, '%s' % ep_without_space)
