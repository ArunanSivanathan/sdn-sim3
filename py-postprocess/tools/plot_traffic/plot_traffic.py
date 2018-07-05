import csv
import matplotlib.pyplot as plt


class PlotTraffic:
    def __init__(self, traffic_file, tid_col):
        self.file = traffic_file;
        self.tid_col = tid_col

    def get_timeframe_traffic(self, col, start_time, end_time, condtional_col=None, condition=None):
        fid = open(self.file, 'r')
        csv_reader = csv.reader(fid)

        traffic_vect = []
        time_vect = []

        last_time =0;

        line_seek = 0
        for e_l in csv_reader:
            line_seek = line_seek + 1
            if line_seek == 1:
                continue

            if start_time <= int(e_l[self.tid_col]) < end_time:
                if condtional_col is None or (e_l[condtional_col] == condition):
                    time_vect.append(int(e_l[self.tid_col]))
                    traffic_vect.append(int(e_l[col]))

            if condtional_col is None or (e_l[condtional_col] == condition):
                if last_time>int(e_l[self.tid_col]):
                    print(int(e_l[self.tid_col]))
                last_time = int(e_l[self.tid_col])


        fid.close()
        return time_vect, traffic_vect

    def plot(self, tid_vect, traffic_vect, plt_format):
        plt.plot(tid_vect, traffic_vect, plt_format)


def write_windows_in_csv(filename,sample_vector):
    fid = open(filename,'w')
    csv_writer = csv.writer(fid)

    for e_v in sample_vector:
        csv_writer.writerow(e_v)

    fid.close()


if __name__ == "__main__":
    pt = PlotTraffic(
        '/Users/Arunan/Documents/coderepo/sdn-sim3/py-postprocess/of_activity_time_measure/instances/18-07-03.csv', 0)

    boot_time_list = [1530597698]

    device_label = '6'

    sample_vectors= []
    for annotated_time in boot_time_list:
        duration = 30 * 60
        start_time = annotated_time
        end_time = annotated_time + duration

        time_v, traffic_v = pt.get_timeframe_traffic(2, start_time, end_time, -2, device_label)
        time_v = [i - start_time for i in time_v]
        pt.plot(time_v, traffic_v, 'b')

        time_v, traffic_v = pt.get_timeframe_traffic(1, start_time, end_time, -2, device_label)
        time_v = [i - start_time for i in time_v]
        pt.plot(time_v, traffic_v, 'r')

        sample_vectors.append(traffic_v)



        plt.xticks(range(min(time_v),max(time_v),10), rotation='vertical')
        plt.ylabel('bytes/sec')
        plt.show()

    write_windows_in_csv('samples_wemo-Idle.csv',sample_vectors)