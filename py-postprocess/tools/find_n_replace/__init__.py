import re


class FindNReplace:
    def __init__(self,file):
        self.file = file
        self.match = "[.*]+"
        self.replace = "Nothing to replace"

    def find_n_replace_file(self,match,replace,flags=0):
        fid = open(self.file,'r')

        for e_l in fid.readlines():
            if not isinstance(match, list):
                match = [match]
                replace = [replace]

            new_line = e_l
            for e_m,e_r in zip(match,replace):
                new_line = re.sub(e_m,e_r,new_line)


            if new_line!="":
                print(new_line)

    def find_n_list_file(self,match,flags=0):
        output =[];
        fid = open(self.file,'r')

        for e_l in fid.readlines():
            if not isinstance(match, list):
                match = [match]

            for e_m in match:
                output.append( self.find_matches(e_m,e_l))


        return output

    def find_matches(self,pattern,string):
        rex = re.findall(pattern,string,flags=0)
        if rex is None:
            return []
        else:
            return rex


if __name__ == "__main__":
    fr = FindNReplace('/Users/Arunan/Documents/PCAP-Transfer/under_process/activity/new_activities.txt')
    # fr.find_n_replace_file(['.*"sp":(?!53).*\n'],[''])
    fr.find_n_replace_file(['alexa1','dropcam1','netatmowelcome1','samsungsmartcam1','lifx1','wemoswitch1'],['1','9','17','21','14','6'])

    # print(fr.find_n_list_file(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'))