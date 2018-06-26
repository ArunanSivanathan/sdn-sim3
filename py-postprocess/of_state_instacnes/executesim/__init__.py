import subprocess

SDNSIM = '../../cmake-build-debug/sdn_sim3'

def execute_sim(pcap_file):
    print( ' '.join(['/Users/Arunan/Documents/coderepo/sdn-sim3/cmake-build-debug/sdn_sim3',pcap_file, '0']))
    subprocess.call(['/Users/Arunan/Documents/coderepo/sdn-sim3/cmake-build-debug/sdn_sim3',pcap_file, '0'],cwd='../../cmake-build-debug/')
    # subprocess.call(['sdn_sim3', pcap_file, '0'],cwd='../../cmake-build-debug/')
