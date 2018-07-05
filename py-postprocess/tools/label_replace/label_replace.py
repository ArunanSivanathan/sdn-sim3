import csv

class LabelReplace():
    def __init__(self, src_file):
        self.src_file = src_file

    def replace_labels(self,filter_col,matching_replace_dict,output_file):
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


            new_label = matching_replace_dict.get(e_l[filter_col],None)
            if new_label: #If there is a replacement
                e_l[filter_col] = new_label
            csv_writer.writerow(e_l)

        fid_input.close()


if __name__=="__main__":
    fi = LabelReplace('/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/iot_vs_noniot_instances/out_temp/dev_id_full_data-training.csv')
    fi.replace_labels(-1,{'1':98,'2':98,'3':98, '5':98, '6':98, '9':98, '12':98, '14':98, '15':98, '16':98,'17':98, '18':98, '21':98, '22':98, '25':98, '26':98, '28':98},'./non-IoT.csv')