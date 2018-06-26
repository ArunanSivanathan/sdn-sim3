import os
import tools.weka_processing.wekatools as weka

def make_arff_file():
    # csv_files = ['testing-all', 'testing-dec','testing-feb','testing-jan','testing-march','training']
    # csv_files = ['states_belkin_cam','states_canary','states_dropcam','states_lifx','states_smartcam','states_tpswitch']
    # csv_files = ['lifx-testing','lifx-training']
    # csv_files = ['testing-3month-include-feb','training-3month-include-feb']
    # csv_files = ['non-IoT','testing-3month-include-feb','training-3month-include-feb','training-3month-without-feb','testing-3month-without-feb']
    # csv_files = ['activity_amazonecho','activity_belkinswitch','activity_dropcam','activity_lifx','activity_netwelcome','activity_smartcam']
    csv_files = ['amazonecho-testing','amazonecho-training','belkinswitch-testing','belkinswitch-training','dropcam-testing','dropcam-training','lifx-testing','lifx-training',]

    for cf in csv_files:
        weka.preprocess_makeNominalCols('/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/tools/split_instances/csv/%s.csv'%cf,'./arff_files/%s.arff'%cf,'last')
        # weka.remove_attributes('./arff_files/%sx.arff'%cf,'./arff_files/%s.arff'%cf,'first')
        # os.remove('./arff_files/%sx.arff'%cf)


if __name__ == "__main__":
    make_arff_file()