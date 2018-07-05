"""
This script is just to automate activity classification of each devices classification
Lot of manual configurations are inside each function
If you want to tweek something make a copy of this code and do it.
Do not edit this code unless you are never going to use iot vs non-iot classification on this way
"""


# Todo: identify activitiy offset from annotations

def merge_all_instances():
    ##########################Merge all activity instances of all devices##########################
    activity_all = ['18-06-14', '18-06-26']

    src_filepaths = [
        '/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/of_activity_instances/instances/%s.csv' % fn
        for fn in activity_all]

    from tools.merge_instances.merge_instance import MergeInstances

    merge_ins = MergeInstances(src_filepaths, './out_temp/activity-instances-all.csv', 0)
    merge_ins.merge_instance()
    ##########################Merge all activity instances of all devices##########################

def split_activity_instances_by_dev():
    file_names = {'1': './out_temp/activity_amazonecho.csv',
                  '6': './out_temp/activity_belkinswitch.csv',
                  '9': './out_temp/activity_dropcam.csv',
                  '14': './out_temp/activity_lifx.csv'}

    from tools.split_activity_instance_by_dev.split_activity_instance_by_dev import SplitActivityInstancesDevSpecific
    state_instance = SplitActivityInstancesDevSpecific('./out_temp/activity-instances-all.csv', -2)
    state_instance.write_to_file(file_names)


def split_training_testing():
    from tools.split_instances.split_instances import SplitInstances

    base_url = './out_temp'
    file_vector = ['activity_amazonecho','activity_belkinswitch','activity_dropcam','activity_lifx']

    for file in file_vector:
        fni = SplitInstances('%s/%s.csv' % (base_url, file),-1)
        instance_count = fni.__instance_count__()

        train_portion = {k:40 for k,v in instance_count.items() }
        outfilenames = "./out_temp/%s-%s.csv"
        fni.split_n(train_portion, outfilenames % ('training',file), outfilenames % ('testing',file))


def test_on_weka():
    from tools.weka_processing import wekatools as weka

    dataset_vector = ['activity_amazonecho', 'activity_belkinswitch', 'activity_dropcam', 'activity_lifx']

    for e_d in dataset_vector:
        data_files = [ '%s-%s' % ('training',e_d), '%s-%s' % ('testing',e_d)]

        # make arff files with norminal values
        for cf in data_files:
            weka.preprocess_makeNominalCols('./out_temp/%s.csv' % cf, './out_temp/%s.arff' % cf, 'last')

        outfile = './out_temp/prediction-%s.csv' % e_d
        # get the prediction without timestamp attribute which is placed as first col
        weka.Randomforest_predict_instances('./out_temp/%s-%s.arff' % ('training',e_d),
                                            './out_temp/%s-%s.arff' % ('testing',e_d), outfile, 'first')


def print_confusion():
    from tools.gen_confusion_matrix.gen_confusion_matrix import LoadPredictionFile, GenConfusionMatrix, \
        PlotConfidentHist

    prediction_vector = ['activity_amazonecho', 'activity_belkinswitch', 'activity_dropcam', 'activity_lifx']

    for e_p  in prediction_vector:
        print("\n\n\nConfusion martix of %s"%e_p)
        lp = LoadPredictionFile('./out_temp/prediction-%s.csv'%e_p)
        cm = GenConfusionMatrix(lp.get_prediction_matrix(), ['3', '2','1'])
        cm.print_confusion_matrix(show_percentage=True,print_labels=False, format='%.02f')

        pch = PlotConfidentHist(lp.get_prediction_matrix())
        pch.plot_confident_hist()


if __name__ == "__main__":
    run_events = {'merge_all_instances': 0, 'split_activity_instance_dev_specific': 0, 'split_training_testing': 0, 'test_on_weka': 0, 'print_confusion': 1}

    if run_events['merge_all_instances'] == 1:
        merge_all_instances()

    if run_events['split_activity_instance_dev_specific'] == 1:
        split_activity_instances_by_dev()

    if run_events['split_training_testing'] == 1:
        split_training_testing()

    if run_events['test_on_weka'] == 1:
        test_on_weka()

    if run_events['print_confusion'] == 1:
        print_confusion()
