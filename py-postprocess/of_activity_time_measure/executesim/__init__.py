import subprocess

SDNSIM = '../../cmake-build-debug/sdn_sim3'


def execute_sim(resolution, pcap_file, flow_entry_file):
    cmd = ['/Users/Arunan/Documents/coderepo/sdn-sim3/cmake-build-debug/sdn_sim3', '--verbose', '-r', str(resolution)
        , pcap_file, 'simplestatic', '--', '--flowentries', flow_entry_file]
    print(' '.join(cmd))
    subprocess.call(cmd, cwd='../../cmake-build-debug/')
    # subprocess.call(['sdn_sim3', pcap_file, '0'],cwd='../../cmake-build-debug/')
