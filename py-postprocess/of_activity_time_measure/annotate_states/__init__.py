import csv

COL_CLASS = 0
COL_ACTIVITY = 1
COL_TIME = 2

class AnnotateStates:
    def __init__(self, annotation_files, annotation_margin_dict):
        self.annotation_files = annotation_files

        self.annotation_hash = {}
        self.annotation_margin_dict = annotation_margin_dict

        self.instance_duration = 1 * 60

        self.load_state_files()

    def load_state_files(self):

        for e_f in self.annotation_files:
            fid = open(e_f, 'r')
            csv_reader = csv.reader(fid)

            #state_annotation_file should be formatted as  device class, activity, tid

            for e_l in csv_reader:
                c_class = e_l[COL_CLASS]
                c_activity = e_l[COL_ACTIVITY]
                c_time = int(float(e_l[COL_TIME]))

                if c_class not in self.annotation_hash:
                    self.annotation_hash[c_class]={}

                activity_start = c_time + self.annotation_margin_dict[c_class][c_activity][0]
                activity_end= c_time + self.annotation_margin_dict[c_class][c_activity][1]

                for e_tid in range(activity_start,activity_end):
                    self.annotation_hash[c_class][e_tid]=c_activity

    def annotate(self,device_id,tid):
        tid=int(tid)
        last_known_state = None

        # if device_id=='17' and tid>1528992500 and tid-self.state_margin_time<1528992500:
        #     print('found')

        for event_time in range(tid, tid-self.instance_duration, -1):
            last_known_state = self.annotation_hash[device_id].get(event_time,None)
            if last_known_state is not None:
                break

        if last_known_state is None:
            last_known_state='idle'

        return last_known_state