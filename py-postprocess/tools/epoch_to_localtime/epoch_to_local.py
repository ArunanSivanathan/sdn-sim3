import csv
import time;

class EpochToLocal:
    def convert_from_file(self,filename,col_no = 0,format = "%a, %d %b %Y %H:%M:%S %z"):
        converted_rows = []
        fid = open(filename,'r')
        csv_reader = csv.reader(fid)

        for e_l in csv_reader:
            converted_rows.append(e_l)
            converted_rows[-1].append( self.convert_time(float(converted_rows[-1][col_no]),format))
            # converted_rows[-1][col_no] = self.convert_time(float(converted_rows[-1][col_no]),format)

        fid.close()
        return converted_rows


    def convert_time(self,epoch_time,format = "%a, %d %b %Y %H:%M:%S %z" ):
        return time.strftime(format, time.localtime(epoch_time))

import datetime
if __name__ == "__main__":
    tc = EpochToLocal()
    converted_rows = tc.convert_from_file("/Users/Arunan/Documents/PCAP-Transfer/under_process/activity/activity_annotation.txt",col_no =2,format = "%m/%d")
    [print(rows) for rows in converted_rows]
