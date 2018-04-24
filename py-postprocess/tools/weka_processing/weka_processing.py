import wekatools as weka

def make_arff_file():
    # csv_files = ['testing-all', 'testing-dec','testing-feb','testing-jan','testing-march','training']
    csv_files = ['testing-3month', 'training-3month']

    for cf in csv_files:
        weka.preprocess_makeNominalCols('../merge_instances/%s.csv'%cf,'./%s.arff'%cf,'last')

if __name__=="__main__":
    make_arff_file()
    # make_arff_file()