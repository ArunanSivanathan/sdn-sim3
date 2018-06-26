import os, csv
import re
WEKA_CLASSPATH = "/Applications/weka-3-8-0-oracle-jvm.app/Contents/Java/weka.jar"


def convert2arff(inFile, outFile):
    command = "java  -cp " + WEKA_CLASSPATH + \
              " weka.core.converters.CSVLoader " + inFile + \
              " -B 2000 > " + outFile
    print(command)
    os.system(command)


def preprocess_addID(inFile, outFile):
    command = "java  -cp " + WEKA_CLASSPATH + \
              " weka.filters.unsupervised.attribute.AddID -C first -N ID " + \
              " -i " + inFile + \
              " -o " + outFile
    print(command)
    os.system(command)


def preprocess_make_lastcol_Nominal(inFile, outFile):
    command = "java  -cp " + WEKA_CLASSPATH + \
              " weka.filters.unsupervised.attribute.NumericToNominal -R last" + \
              " -i " + inFile + \
              " -o " + outFile
    print(command)
    os.system(command)


def preprocess_makeNominalCols(inFile, outFile, attributeNos):
    command = "java  -cp " + WEKA_CLASSPATH + \
              " weka.filters.unsupervised.attribute.NumericToNominal -R " + attributeNos + \
              " -i " + inFile + \
              " -o " + outFile
    print(command)
    os.system(command)


def classify_naivebayes(inFile, outFile, dist=False):
    if dist == True:
        distribution = " -distribution"
    else:
        distribution = ""

    command = "java -cp " + WEKA_CLASSPATH + \
              " weka.classifiers.meta.FilteredClassifier" + \
              " -F \"weka.filters.unsupervised.attribute.Remove -R 1\"" + \
              " -W weka.classifiers.bayes.NaiveBayesMultinomial" + \
              " -t " + inFile + \
              " -classifications \"weka.classifiers.evaluation.output.prediction.CSV " + distribution + " -p first -file " + outFile + "\" >/dev/null 2>&1"
    print(command)
    os.system(command)


def classify_J48(inFile, outFile):
    command = "java -cp " + WEKA_CLASSPATH + \
              " weka.classifiers.meta.FilteredClassifier" + \
              " -F \"weka.filters.unsupervised.attribute.Remove -R 1\"" + \
              " -W weka.classifiers.trees.J48" + \
              " -t " + inFile + \
              " -classifications \"weka.classifiers.evaluation.output.prediction.CSV -p first -file " + outFile + "\""
    print(command)
    os.system(command)


def sort_csv(inFile, outFile):
    reader = csv.DictReader(open(inFile, 'r'))
    result = sorted(reader, key=lambda d: float(d['ID']))

    # for each in result:
    # 	print each

    writer = csv.DictWriter(open(outFile, 'w'), reader.fieldnames)
    writer.writeheader()
    writer.writerows(result)


def remove_range(inFile, outFile, indexRange):
    command = "java  -cp " + WEKA_CLASSPATH + \
              " weka.filters.unsupervised.instance.RemoveRange -R " + indexRange + \
              " -i " + inFile + \
              " -o " + outFile
    print(command)
    os.system(command)


def classify_Randomforest(trainFile, testFile, outFile, removeAttributes):
    # weka.classifiers.meta.FilteredClassifier -F "weka.filters.unsupervised.attribute.Remove -R 8,9" -W weka.classifiers.misc.InputMappedClassifier -- -I -trim -W weka.classifiers.trees.RandomForest -- -P 100 -I 100 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 1

    command = "java -cp " + WEKA_CLASSPATH + \
              " weka.classifiers.meta.FilteredClassifier" + \
              " -t " + trainFile + \
              " -T " + testFile + \
              " -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file " + outFile + " -suppress\"" + \
              " -F \"weka.filters.unsupervised.attribute.Remove -R " + removeAttributes + "\"" \
                                                                                          " -W weka.classifiers.misc.InputMappedClassifier -- -I -trim " + \
              " -W weka.classifiers.trees.RandomForest -- -P 100 -I 100 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 1"
    print(command)
    os.system(command)

def classify_Randomforest_evaluation(trainFile, testFile, outFile, removeAttributes):
    # weka.classifiers.meta.FilteredClassifier -F "weka.filters.unsupervised.attribute.Remove -R 8,9" -W weka.classifiers.misc.InputMappedClassifier -- -I -trim -W weka.classifiers.trees.RandomForest -- -P 100 -I 100 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 1

    if removeAttributes!="":
        command = "java -cp " + WEKA_CLASSPATH + \
                  " weka.classifiers.meta.FilteredClassifier" + \
                  " -t " + trainFile + \
                  " -T " + testFile + \
                  " -F \"weka.filters.unsupervised.attribute.Remove -R " + removeAttributes + "\"" \
                  " -W weka.classifiers.misc.InputMappedClassifier -- -I -trim " + \
                  " -W weka.classifiers.trees.RandomForest -- -P 100 -I 100 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 1 >" + outFile

    else:
        command = "java -cp " + WEKA_CLASSPATH + \
                  "  weka.classifiers.trees.RandomForest -P 100 -I 100 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 1 " + \
                  " -t " + trainFile + \
                  " -T " + testFile + \
                  " >" + outFile
    print(command)
    os.system(command)
def findAccuracyRRSE(evauation_file):

    accuracy=None
    rrse=None

    with open(evauation_file, 'r') as fid:
        on_test=0;
        for line in fid:

            if on_test ==0:
                m = re.search("=== Error on test data ===", line)
                if m is not None:
                    on_test=1
            elif on_test ==1:
                m = re.search("(^Correctly Classified Instances\W+\d+\W+)([\d\.]+)", line)
                if m is not None:
                    accuracy= m.groups()[1]

                m = re.search("(^Root relative squared error\W+)([\d\.]+)", line)
                if m is not None:
                    rrse = m.groups()[1]

    return accuracy, rrse

def get_merit(trainFile, outFile, removeAttributes = None):

    command = "java -cp " + WEKA_CLASSPATH + \
              " weka.attributeSelection.CfsSubsetEval" + \
              " -M" + \
              " -s \"weka.attributeSelection.BestFirst -D 1 -N 5\"" + \
              " -i " + trainFile
    # " -E weka.attributeSelection.InfoGainAttributeEval " + \
    print(command)
    os.system(command)

def get_cfs_subsetevaluation(trainFile, outFile, removeAttributes = None):

    command = "java -cp " + WEKA_CLASSPATH + \
              " weka.attributeSelection.CfsSubsetEval" + \
              " -M" + \
              " -s \"weka.attributeSelection.BestFirst -D 1 -N 5\"" + \
              " -i " + trainFile
    # " -E weka.attributeSelection.InfoGainAttributeEval " + \
    print(command)
    os.system(command)