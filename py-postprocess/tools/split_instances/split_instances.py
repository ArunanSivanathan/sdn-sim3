import csv
import random


class SplitInstances:
    def __init__(self,filename,class_col=-1):
        self.filename = filename
        self.class_col=class_col

    def split_first_n(self, split_counts, first_output, second_output):
        fid = open(self.filename,'r')
        csv_reader = csv.reader(fid)

        class_count = {}

        f_writer1 = open(first_output,'w')
        f_writer2 = open(second_output,'w')

        csv_writer1 = csv.writer(f_writer1)
        csv_writer2 = csv.writer(f_writer2)

        line_seek = 0
        for e_l in csv_reader:
            line_seek=line_seek+1
            if line_seek==1:
                csv_writer1.writerow(e_l)
                csv_writer2.writerow(e_l)
                continue

            current_class = e_l[self.class_col]
            class_count[current_class]= class_count.get(current_class,0)+1

            if class_count[current_class]<split_counts[current_class]:
                csv_writer1.writerow(e_l)
            else:
                csv_writer2.writerow(e_l)

        f_writer1.close()
        f_writer2.close()
        fid.close()

    def split_class_rows(self):
        fid = open(self.filename,'r')
        csv_reader = csv.reader(fid)

        class_count = {}

        line_seek = 0
        for e_l in csv_reader:
            line_seek=line_seek+1
            if line_seek==1:
                continue

            current_class = e_l[self.class_col]
            if current_class not in class_count.keys():
                class_count[current_class]=[]


            class_count.get(current_class).append(line_seek)
        return class_count

    def split_n(self, split_counts, first_output, second_output):

        #get rondom train and split portions
        dict_class_rows = self.split_class_rows()

        train_lines = []
        test_lines = []

        for each in dict_class_rows.keys():
            random.shuffle(dict_class_rows[each])
            train_lines.extend(dict_class_rows[each][0:split_counts[each]])
            test_lines.extend(dict_class_rows[each][split_counts[each]:])


        train_lines.sort()
        test_lines.sort()
        # get rondom train and split portions

        fid = open(self.filename,'r')
        csv_reader = csv.reader(fid)

        f_writer1 = open(first_output,'w')
        f_writer2 = open(second_output,'w')

        csv_writer1 = csv.writer(f_writer1)
        csv_writer2 = csv.writer(f_writer2)

        line_seek = 0
        for e_l in csv_reader:
            line_seek=line_seek+1
            if line_seek==1:
                csv_writer1.writerow(e_l)
                csv_writer2.writerow(e_l)
                continue


            if len(train_lines)> 0 and line_seek == train_lines[0]:
                del(train_lines[0])
                csv_writer1.writerow(e_l)
            elif len(test_lines)> 0 and line_seek == test_lines[0]:
                del (test_lines[0])
                csv_writer2.writerow(e_l)
            else:
                raise("Error or split n")

        f_writer1.close()
        f_writer2.close()
        fid.close()

    def __instance_count__(self):
        fid = open(self.filename,'r')
        csv_reader = csv.reader(fid)
        class_count = {}

        line_seek = 0
        for e_l in csv_reader:
            line_seek=line_seek+1
            if line_seek==1:
                continue

            current_class = e_l[self.class_col]
            class_count[current_class]= class_count.get(current_class,0)+1

        return class_count


if __name__ == "__main__":
    base_url='/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/iot_vs_noniot_instances/data/'
    file_vector = ['device_identification_full_dataset']

    for file in file_vector:
        fni = SplitInstances('%s/%s.csv' % (base_url, file))
        instance_count = fni.__instance_count__()

        # train_portion = {k:v*0.66 for k,v in instance_count.items() }
        # train_portion = {k:40 for k,v in instance_count.items() }
        train_portion = {'1':50,'2':50,'3':50, '5':50, '6':50, '9':50, '12':50, '14':50, '15':50, '16':50,'17':50, '18':50, '21':50, '22':50, '25':50, '26':50, '28':50, '99': 800}
        # train_portion = {k:40 for k,v in instance_count.items() }
        fni.split_n(train_portion,'./csv/%s-training.csv'%file, './csv/%s-testing.csv'%file)