import csv
import re

import wekatools as weka


class MultipleTesting:
    def __init__(self,model, training_file,testing_file_list,arff_conversion=True):
        self.training_file = training_file
        self.testing_file_list = testing_file_list
        self.arff_conversion=arff_conversion
        self.model = model
        self.output = './output.txt'

    def convert_to_arff(self,file_name):
        tmp_test_file='./tmp_test.arff'
        weka.preprocess_makeNominalCols( file_name,tmp_test_file,'last')
        return tmp_test_file

    def get_results_list(self,device_filter=None):
        fid = open(self.output,'w')
        csv_writer = csv.writer(fid)

        results_vector = {}

        for e_file in self.testing_file_list:
            if self.arff_conversion == True:
                test_file = self.convert_to_arff(e_file)
            else:
                test_file = e_file

            wekaoutput = weka.Randomforest_load_and_test(self.model,'../weka_processing/training-3month.arff',test_file)

            results_vector[e_file] = self.find_TP_Device(wekaoutput,12)
            print('%s\t%s\t%s'%(e_file,results_vector[e_file][0],results_vector[e_file][1]))
            csv_writer.writerow([e_file,results_vector[e_file][0],results_vector[e_file][1]])
            fid.flush()

        fid.close()
        return results_vector

    def find_TP_Device(self,evauation_txt,device_id):

        tp = None
        confmapline = None

        on_test = 0;
        for line in evauation_txt:

            if on_test == 0:
                m = re.search("=== Error on test data ===", line)
                if m is not None:
                    on_test = 1
            elif on_test == 1:
                m = re.search("^ +([\d\.\?]+) +([\d\.\?]+) +([\d\.\?]+) +([\d\.\?]+) +([\d\.\?]+) +([\d\.\?]+) +([\d\.\?]+) +([\d\.\?]+) +%d$"%device_id, line)
                if m is not None:
                    tp = m.groups()[0]

                m2 = re.search("^( +[\d]+){17}(.*)%d$" % device_id,
                        line)
                if m2 is not None:
                    confmapline = m2.string


        return tp, confmapline



if __name__ == "__main__":
    test_files = ['17-01-01', '17-01-02', '17-01-03', '17-01-04', '17-01-05',
                 '17-01-06', '17-01-07', '17-01-08', '17-01-09', '17-01-10', '17-01-11', '17-01-12', '17-01-13',
                 '17-01-14', '17-01-16', '17-01-17', '17-01-18', '17-01-19', '17-01-20', '17-01-21', '17-01-22',
                 '17-01-23', '17-01-24', '17-01-25', '17-01-26', '17-01-27', '17-01-28', '17-01-29', '17-01-30',
                 '17-01-31', '17-02-01', '17-02-03', '17-02-04', '17-02-05', '17-02-06', '17-02-07', '17-02-08',
                 '17-02-09', '17-02-10', '17-02-11', '17-02-12', '17-02-13', '17-02-14', '17-02-15', '17-02-16',
                 '17-02-17', '17-02-18', '17-02-19', '17-01-15', '17-02-02', '17-02-20', '17-03-10', '17-02-21',
                 '17-02-22', '17-02-23', '17-02-24', '17-02-25', '17-02-26', '17-02-27', '17-02-28', '17-03-01',
                 '17-03-02', '17-03-03', '17-03-04', '17-03-05', '17-03-06', '17-03-07', '17-03-08', '17-03-09',
                 '17-03-11', '17-03-12', '17-03-13', '17-03-14', '17-03-15', '17-03-16', '17-03-17', '17-03-18',
                 '17-03-19', '17-03-20', '17-03-21', '17-03-22', '17-03-23', '17-03-24', '17-03-25', '17-03-26',
                 '17-03-27', '17-03-28', '17-03-29', '17-03-30', '17-03-31']

    test_filepaths = ['/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/of_dev_instances/instances/%s.csv' % fn
                     for fn in test_files]

    mt = MultipleTesting('./tmp_model.model','../weka_processing/training-3month.arff',test_filepaths)
    results = mt.get_results_list()
    for e_day in test_files:
        full_path = '/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/of_dev_instances/instances/%s.csv' % e_day
        print('%s-%s'%(e_day,results[full_path]))

