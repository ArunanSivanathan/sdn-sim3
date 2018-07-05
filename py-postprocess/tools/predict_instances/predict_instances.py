import tools.weka_processing.wekatools as weka


if __name__=="__main__":
    weka.Randomforest_predict_instances(
        "/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/tools/weka_processing/arff_files/training-3month-include-feb.arff",
        "/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/tools/weka_processing/arff_files/non-IoT.arff",
        "./predict-non-IoT.csv",'1')