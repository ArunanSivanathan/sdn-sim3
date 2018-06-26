import os


class LimitPCAPTime:
    def __init__(self,starttime,endtime):
        self.start_time = starttime
        self.end_time = endtime

    def limit_pcap_time(self,input_file,output_file):
        command = ["editcap", "-S","0.000001","-A", "\"%s\""%self.start_time, "-B", "\"%s\""%self.end_time, input_file, output_file]
        print(" ".join(command))
        os.system(" ".join(command))

if __name__ == '__main__':
    files = ['18-02-25', '18-02-26']
    full_output_path = ["/Volumes/iot_backup/states-last-filtered/%s.pcap"%p for p in files]
    full_input_path = ["/Volumes/iot_backup/states-last-franco/%s.pcap"%p for p in files]

    lpcap = LimitPCAPTime("2018-01-01 00:00:00","2018-03-31 23:59:59")

    for i_p,o_p in zip(full_input_path,full_output_path):
        lpcap.limit_pcap_time(i_p,o_p)