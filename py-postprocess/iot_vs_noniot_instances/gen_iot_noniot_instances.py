"""
This script is just to automate iot vs non-iot classification
Lot of manual configurations are inside each function
If you want to tweek something make a copy of this code and do it.
Do not edit this code unless you are never going to use iot vs non-iot classification on this way
"""

def merge_all_instances():
    #########################Merge all instances (avoid attack traffic) (iot_vs_noniot_instances/data/device_identification_full_dataset.csv)##########################
    attack_days = ['16-10-05','16-10-14','16-11-14','16-11-17','16-11-28','16-12-05','16-12-06','16-12-07','16-12-08','16-12-09','16-12-10','16-12-11','16-12-12','16-12-13','16-12-14','16-12-15','16-12-16','16-12-17','16-12-18','16-12-19','16-12-20','16-12-21','16-12-22','16-12-23','16-12-24','17-01-02','17-01-10','17-01-12','17-01-29','17-01-30','17-01-31','17-02-02','17-02-06','17-02-07','17-02-08','17-02-09','17-02-10','17-02-14','17-02-20','17-02-22','17-03-01','17-03-02','17-03-03','17-03-07','17-03-08','17-03-09','17-03-10','17-03-14','17-03-16','17-03-23','17-03-27']

    all_days = ['16-10-01', '16-10-02', '16-10-03', '16-10-04', '16-10-05', '16-10-06', '16-10-07', '16-10-08',
                 '16-10-09', '16-10-10', '16-10-11', '16-10-12', '16-10-13', '16-10-14', '16-10-15', '16-10-16',
                 '16-10-17', '16-10-18', '16-10-19', '16-10-20', '16-10-21', '16-10-22', '16-10-23', '16-10-24',
                 '16-10-25', '16-10-26', '16-10-27', '16-10-28', '16-10-29', '16-10-30', '16-10-31', '16-11-01',
                 '16-11-02', '16-11-03', '16-11-04', '16-11-05', '16-11-06', '16-11-07', '16-11-08', '16-11-09',
                 '16-11-10', '16-11-11', '16-11-12', '16-11-13', '16-11-14', '16-11-15', '16-11-16', '16-11-17',
                 '16-11-18', '16-11-19', '16-11-20', '16-11-21', '16-11-22', '16-11-23', '16-11-24', '16-11-25',
                 '16-11-26', '16-11-27', '16-11-28', '16-11-29', '16-11-30', '16-12-01', '16-12-02', '16-12-03',
                 '16-12-04', '16-12-05', '16-12-06', '16-12-07', '16-12-08', '16-12-09', '16-12-10', '16-12-11',
                 '16-12-12', '16-12-13', '16-12-14', '16-12-17', '16-12-18', '16-12-19', '16-12-20',
                 '16-12-21', '16-12-22', '16-12-23', '16-12-24', '16-12-25', '16-12-26', '16-12-27', '16-12-28',
                 '16-12-29', '16-12-30', '16-12-31','17-01-01', '17-01-02', '17-01-03', '17-01-04', '17-01-05',
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

    all_days = [x for x in all_days if x not in attack_days]
    all_days = ['/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/of_dev_instances/instances/%s.csv' % fn
                     for fn in all_days]

    from tools.merge_instances.merge_instance import MergeInstances

    merge_ins = MergeInstances(all_days, './out_temp/device_identification_full_dataset.csv', 15)
    merge_ins.merge_instance()
    #########################Merge all instances (avoid attack traffic) (iot_vs_noniot_instances/data/device_identification_full_dataset.csv)##########################

def get_raw_instance_count():
    from tools.instance_count.instance_count import InstanceCounter,plot_bar,ordered_values
    import tools.instance_count.visuals as visuals

    ic = InstanceCounter('./out_temp/full_ds-device_identification.csv')
    ic_value_dict = ic.count_instance()

    plot_order = ['1', '2', '3', '5', '6', '9', '12', '14', '15', '16', '17','18', '21', '22', '25', '26', '28','99']
    device_names = {'1':'Amazon Echo', '2':'August Doorbell', '3':'Awair air quality', '5':'Belkin Motion Sensor',
                    '6':'Belkin Switch', '9':'Dropcam', '12':'HP Printer', '14':'LiFX Bulb', '15':'NEST Smoke Sensor',
                    '16':'Netatmo Weather', '17':'Netatmo Camera', '18':'Hue Bulb', '21':'Samsung Smart Camera',
                    '22':'Smart Things', '25':'Triby Speaker', '26':'Withings sleep sensor', '28':'Withings Scale',
                    '99': 'Non-IoT'}

    bar_heights = ordered_values(ic_value_dict,plot_order)
    device_labels = ordered_values(device_names,device_names)
    filename='raw_instances'
    plot_bar(bar_heights,device_labels,'Number of Instances',filename='./out_temp/instance-count-%s.png'%filename)

def split_training_testing():
    from tools.split_instances.split_instances import SplitInstances

    base_url='./out_temp/device_identification_full_dataset.csv'
    fni = SplitInstances(base_url, -1)

    train_portion = {'1':50,'2':50,'3':50, '5':50, '6':50, '9':50, '12':50, '14':50, '15':50, '16':50,'17':50, '18':50, '21':50, '22':50, '25':50, '26':50, '28':50, '99': 800}
    outfilenames = "./out_temp/%s-dev_id_full_data.csv"
    fni.split_n(train_portion,outfilenames%'training', outfilenames%'testing')

def replace_labels():
    from tools.label_replace.label_replace import LabelReplace
    outputfilenames = './out_temp/%s-iot-noniot.csv'

    training = LabelReplace('./out_temp/dev_id_full_data-training.csv')
    training.replace_labels(-1,{'1':98,'2':98,'3':98, '5':98, '6':98, '9':98, '12':98, '14':98, '15':98, '16':98,'17':98, '18':98, '21':98, '22':98, '25':98, '26':98, '28':98},outputfilenames%'training')

    testing = LabelReplace('./out_temp/dev_id_full_data-testing.csv')
    testing.replace_labels(-1,{'1':98,'2':98,'3':98, '5':98, '6':98, '9':98, '12':98, '14':98, '15':98, '16':98,'17':98, '18':98, '21':98, '22':98, '25':98, '26':98, '28':98},outputfilenames%'testing')

def test_on_weka():
    from tools.weka_processing import wekatools as weka
    csv_files = ['non-IoT-training','non-IoT-testing']

    #make arff files with norminal values
    for cf in csv_files:
        weka.preprocess_makeNominalCols('./out_temp/%s.csv' % cf,'./out_temp/%s.arff' % cf, 'last')
    outfile = './out_temp/prediction-%s.csv'%'iot-noniot'
    #get the prediction without timestamp attribute which is placed as first col
    weka.Randomforest_predict_instances('./out_temp/%s.arff'%'non-IoT-training','./out_temp/%s.arff'%'non-IoT-testing',outfile,'first')

def print_confusion():
    from tools.gen_confusion_matrix.gen_confusion_matrix import LoadPredictionFile,GenConfusionMatrix,PlotConfidentHist
    lp = LoadPredictionFile('/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/iot_vs_noniot_instances/out_temp/prediction-iot-noniot.csv')
    cm = GenConfusionMatrix(lp.get_prediction_matrix(),['98','99'])
    cm.print_confusion_matrix(print_labels=False,format='%.02f')

    pch = PlotConfidentHist(lp.get_prediction_matrix())
    pch.plot_confident_hist()

if __name__ =="__main__":
    run_events={'merge_all_instances':0,'raw_instance_count':0,'split_training_testing':0,'replace_labels':0,'test_on_weka':0,'print_confusion':1}

    if run_events['merge_all_instances']==1:
        merge_all_instances()
        
    if run_events['raw_instance_count']==1:
        get_raw_instance_count()

    if run_events['split_training_testing']==1:
        split_training_testing()

    if run_events['replace_labels']==1:
        replace_labels()

    if run_events['test_on_weka']==1:
        test_on_weka()

    if run_events['print_confusion']==1:
        print_confusion()