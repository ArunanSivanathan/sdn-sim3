import csv


class AnnotateStates:
    def __init__(self,states_annotation):
        self.state_annotation_file = states_annotation
        self.state_dict = {}
        self.state_margin_time = 1*60

        self.load_state_files()

    def load_state_files(self):
        fid = open(self.state_annotation_file,'r')
        csv_reader = csv.reader(fid)

        self.state_dict = {}
        for e_l in csv_reader:
            if e_l[0] not in self.state_dict:
                self.state_dict[e_l[0]]={}

            self.state_dict[e_l[0]][int(float(e_l[2]))]=e_l[1]

    def annotate(self,device_id,tid):
        tid=int(tid)
        last_known_state = None

        # if device_id=='17' and tid>1528992500 and tid-self.state_margin_time<1528992500:
        #     print('found')

        for event_time in range(tid,tid-self.state_margin_time,-1):
            last_known_state = self.state_dict[device_id].get(event_time,None)
            if last_known_state is not None:
                break

        if last_known_state is None:
            last_known_state='idle'

        return last_known_state