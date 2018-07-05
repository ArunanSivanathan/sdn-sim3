import subprocess

SDNSIM = '../../cmake-build-debug/sdn_sim3'


def execute_sim(resolution, pcap_file):
    cmd = ['/Users/Arunan/Documents/coderepo/sdn-sim3/cmake-build-debug/sdn_sim3', '--verbose', '-r', str(resolution)
        , pcap_file, 'ofdc']
    print(' '.join(cmd))
    subprocess.call(cmd, cwd='../../cmake-build-debug/')