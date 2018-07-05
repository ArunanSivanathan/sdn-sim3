import csv

class GenConfusionMatrix:
    def __init__(self,prediction_matrix,labels=None):
        self.actual_list = prediction_matrix['actual']
        self.prediction_list = prediction_matrix['prediction']

        self.labels = list(set(self.actual_list))
        if labels:
            if len(self.labels) > len(labels):
                raise("actual data contains more cols than provided labels")
            else:
                self.labels = labels

    def get_confusion_matrix(self,show_percentage=False):
        confusion_count = {actual:{predict:0for predict in self.labels} for actual in self.labels}
        for a,p in zip(self.actual_list, self.prediction_list):
            confusion_count[a][p]=confusion_count[a][p]+1

        if show_percentage==True:
            for a in self.labels:
                total_ins = sum(confusion_count[a].values())
                for p in self.labels:
                    confusion_count[a][p] = confusion_count[a][p]/total_ins if total_ins !=0 else None
        return confusion_count

    def print_confusion_matrix(self,show_percentage=False,print_labels=True,format='%.02f',null_format='-.-'):
        confusion_count = self.get_confusion_matrix(show_percentage)

        if print_labels == True:
            for l in self.labels:
                print ('%s\t'%l,end='')
            print('\n',end='')

        for a in self.labels:
            for p in self.labels:
                if confusion_count[a][p] is not None:
                    print('%s\t'%(format%confusion_count[a][p]),end='')
                else:
                    print('%s\t'%null_format, end='')

            if print_labels == True:
                print('|%s\t' %a)

            print('\n',end='')



class LoadPredictionFile:
    def __init__(self, file):
        self.filename = file
        self.prediction_matrix = {'actual':[], 'prediction':[], 'confidence':[]}
        self.ins_id_available = False
        self.__loadfile__()

    def get_prediction_matrix(self):
        return self.prediction_matrix

    def __loadfile__(self):
        fid = open(self.filename,'r')
        csv_reader = csv.reader(fid)

        line_seek = 0
        for e_l in csv_reader:
            line_seek = line_seek+1
            if line_seek == 1:
                if len(e_l) == 6:
                    ins_id =True
                    self.prediction_matrix['instanceID'] = []
                continue

            if len(e_l)<5:
                break

            self.prediction_matrix['actual'].append(e_l[1].split(':')[1])
            self.prediction_matrix['prediction'].append(e_l[2].split(':')[1])
            self.prediction_matrix['confidence'].append(float(e_l[4]))
            if self.ins_id_available ==True:
                self.prediction_matrix['instanceID'].append(e_l[5])
        fid.close()

class PlotConfidentHist:
    def __init__(self,prediction_matrix):
        self.correct_confident = []
        self.wrong_confident = []

        for a,p,c in zip(prediction_matrix['actual'],prediction_matrix['prediction'],prediction_matrix['confidence']):
            if a == p:
                self.correct_confident.append(c*100)
            else:
                self.wrong_confident.append(c*100)

    def plot_confident_hist(self):
        import random
        import numpy
        from matplotlib import pyplot

        if __name__ == "__main__":
            x = [random.gauss(3, 1) for _ in range(400)]
            y = [random.gauss(4, 2) for _ in range(400)]

            bins = numpy.linspace(0, 100, 100)

            pyplot.hist(self.correct_confident, bins, alpha=0.5, label='Correctly Classified')
            pyplot.hist(self.wrong_confident, bins, alpha=0.5, label='Incorrectly Classified')
            pyplot.legend(loc='upper right')
            pyplot.show()

if __name__ == "__main__":
    lp = LoadPredictionFile('/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/iot_vs_noniot_instances/out_temp/prediction-iot-noniot.csv')
    cm = GenConfusionMatrix(lp.get_prediction_matrix(),['98','99'])
    cm.print_confusion_matrix(show_percentage=True,print_labels=False,format='%.02f')

    pch = PlotConfidentHist(lp.get_prediction_matrix())
    pch.plot_confident_hist()