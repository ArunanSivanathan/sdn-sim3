import csv


class SplitActivityInstancesDevSpecific:
    def __init__(self, file, device_col_no):
        self.filename = file
        self.dev_colno = device_col_no

    def write_to_file(self, output_file_dev_id_map):

        fid = open(self.filename, 'r')
        csv_reader = csv.reader(fid)

        writing_files_id = {}
        csv_writers = {}
        state_dict={'idle':'1','active':'2','boot':'3'}
        for e_dev_id in output_file_dev_id_map.keys():
            writing_files_id[e_dev_id] = open(output_file_dev_id_map[e_dev_id], 'w')
            csv_writers[e_dev_id] = csv.writer(writing_files_id[e_dev_id])

        l_seek = 0
        for e_l in csv_reader:
            l_seek = l_seek + 1
            # new_row = e_l[1:self.dev_colno] + e_l[(self.dev_colno+1):-1]+ [state_dict.get(e_l[-1],e_l[-1])]
            new_row = e_l[0:self.dev_colno] + e_l[(self.dev_colno+1):-1]+ [state_dict.get(e_l[-1],e_l[-1])]

            if l_seek==1:
                [csv_writers[e_dev_id].writerow(new_row) for e_dev_id in output_file_dev_id_map.keys()]
                continue

            device_id = e_l[self.dev_colno]

            if output_file_dev_id_map.get(device_id, None) is not None:
                csv_writers[device_id].writerow(new_row)
            else:
                print("Unknown_device:%s" % str(device_id))

        for e_dev_id in output_file_dev_id_map.keys():
            writing_files_id[e_dev_id].close()


if __name__ == "__main__":
    file_names = {'1': './csv_files/activity_amazonecho.csv',
                  '6': './csv_files/activity_belkinswitch.csv',
                  '9': './csv_files/activity_dropcam.csv',
                  '14': './csv_files/activity_lifx.csv',
                  '17': './csv_files/activity_netwelcome.csv',
                  '21': './csv_files/activity_smartcam.csv'}

    state_instance = SplitActivityInstancesDevSpecific(
        '/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/of_state_instacnes_new_activitybased/instances/18-06-14.csv', -2)
    state_instance.write_to_file(file_names)
