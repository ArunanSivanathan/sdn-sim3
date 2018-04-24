import csv

import wekatools


class AttributeImpact:
    def __init__(self, train_arff, test_arff):
        self.train_arff = train_arff
        self.test_arff = test_arff
        self.attributes_full = ['1minDNSDownCount','2minDNSDownCount','4minDNSDownCount','8minDNSDownCount','16minDNSDownCount','32minDNSDownCount','64minDNSDownCount','1minDNSUpCount','2minDNSUpCount','4minDNSUpCount','8minDNSUpCount','16minDNSUpCount','32minDNSUpCount','64minDNSUpCount','1minNTPDownCount','2minNTPDownCount','4minNTPDownCount','8minNTPDownCount','16minNTPDownCount','32minNTPDownCount','64minNTPDownCount','1minNTPUpCount','2minNTPUpCount','4minNTPUpCount','8minNTPUpCount','16minNTPUpCount','32minNTPUpCount','64minNTPUpCount','1minDNSDownRate','2minDNSDownRate','4minDNSDownRate','8minDNSDownRate','16minDNSDownRate','32minDNSDownRate','64minDNSDownRate','1minDNSUpRate','2minDNSUpRate','4minDNSUpRate','8minDNSUpRate','16minDNSUpRate','32minDNSUpRate','64minDNSUpRate','1minNTPDownRate','2minNTPDownRate','4minNTPDownRate','8minNTPDownRate','16minNTPDownRate','32minNTPDownRate','64minNTPDownRate','1minNTPUpRate','2minNTPUpRate','4minNTPUpRate','8minNTPUpRate','16minNTPUpRate','32minNTPUpRate','64minNTPUpRate','1minLANDownCount','2minLANDownCount','4minLANDownCount','8minLANDownCount','16minLANDownCount','32minLANDownCount','64minLANDownCount','1minLANDownRate','2minLANDownRate','4minLANDownRate','8minLANDownRate','16minLANDownRate','32minLANDownRate','64minLANDownRate','1minANYWANDownCount','2minANYWANDownCount','4minANYWANDownCount','8minANYWANDownCount','16minANYWANDownCount','32minANYWANDownCount','64minANYWANDownCount','1minANYWANDownRate','2minANYWANDownRate','4minANYWANDownRate','8minANYWANDownRate','16minANYWANDownRate','32minANYWANDownRate','64minANYWANDownRate','1minANYWANUpCount','2minANYWANUpCount','4minANYWANUpCount','8minANYWANUpCount','16minANYWANUpCount','32minANYWANUpCount','64minANYWANUpCount','1minANYWANUpRate','2minANYWANUpRate','4minANYWANUpRate','8minANYWANUpRate','16minANYWANUpRate','32minANYWANUpRate','64minANYWANUpRate','1minSSDPUpCount','2minSSDPUpCount','4minSSDPUpCount','8minSSDPUpCount','16minSSDPUpCount','32minSSDPUpCount','64minSSDPUpCount','1minSSDPUpRate','2minSSDPUpRate','4minSSDPUpRate','8minSSDPUpRate','16minSSDPUpRate','32minSSDPUpRate','64minSSDPUpRate',]
        self.attributes_subset = ['8minANYWANUpRate', '64minDNSUpRate', '1minANYWANUpRate', '64minANYWANDownRate',
                                  '32minDNSUpRate', '32minANYWANDownCount', '4minANYWANDownCount', '2minANYWANUpCount',
                                  '16minDNSUpRate', '64minNTPDownCount', '64minSSDPUpCount', '16minLANDownRate']

    def get_instance_id(self, attribute_list):
        indexlist = []
        for e_attribute in attribute_list:
            indexlist.append(self.attributes_full.index(e_attribute)+1)
        return indexlist

    def evaluate_attributes(self, selected_attributes):
        attribute_full_index = range(1, len(self.attributes_full) + 1)
        removed_attribute = [a_id for a_id in attribute_full_index if a_id not in selected_attributes]

        removed_attribute_str = [str(x) for x in removed_attribute]

        print("removed_attributes: %s" % ','.join(removed_attribute_str))
        print("No of removed_attributes: %d" % len(removed_attribute_str))

        removed_attribute_str = ','.join(removed_attribute_str)
        weka_out = wekatools.classify_Randomforest_evaluation(self.train_arff, self.test_arff, './wekaout.tmp.txt',
                                                              removed_attribute_str)

        return wekatools.findAccuracyRRSE('./wekaout.tmp.txt')


if __name__ == "__main__":

    ai = AttributeImpact('../weka_processing/training-3month.arff', '../weka_processing/testing-3month.arff')

    selected_attributes = ai.get_instance_id(ai.attributes_subset)

    fid = open('./accuracyrrse.txt', 'w')
    spam_writer = csv.writer(fid, delimiter=' ')

    for i in range(1, len(selected_attributes) + 1):
        c_attributs = selected_attributes[0:i]
        accuracy, rrse = ai.evaluate_attributes(c_attributs)

        if accuracy is None or rrse is None:
            print("Empty values")
            break

        spam_writer.writerow([i, accuracy, rrse])

    fid.close()
