import csv


class FilterInstances():
    def __init__(self, src_file):
        self.src_file = src_file

    def filter_instance(self,filter_col,filter_val,output_file):
        fid_output = open(output_file, 'w')
        csv_writer = csv.writer(fid_output)

        fid_input = open(self.src_file, 'r')
        csv_reader = csv.reader(fid_input)



        l_seek = 0
        for e_l in csv_reader:
            l_seek = l_seek + 1
            if l_seek == 1:
                csv_writer.writerow(e_l)
                continue

            if e_l[filter_col] in filter_val:
                csv_writer.writerow(e_l)


        fid_input.close()


if __name__=="__main__":
    fi = FilterInstances('/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/tools/merge_instances/full_dataset.csv')
    fi.filter_instance(-1,['99'],'./non-IoT.csv')