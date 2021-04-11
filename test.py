import platform    # For getting the operating system name
import subprocess as sp  # For executing a shell command
import threading
import os

def ping(address, n_echos = 1, wait=2):
    """
    Only tested for Windows and IPv4 address/
    
    Returns True if address (str) responds to a ping request.
    Remember that a address may not respond to a ping (ICMP) request even if the host name is valid.
    Source: https://stackoverflow.com/questions/7678456/local-network-pinging-in-python/14958772
    Inputs:
    - n_echos: Specifies the number of echo Request messages be sent. The default is 1.
    - wait: Specifies the amount of time, in milliseconds, to wait for the echo Reply message corresponding to a given echo Request message. If the echo Reply message is not received within the time-out, the "Request timed out" error message is displayed. 
    Source: https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/ping
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -n 2 -w 2 [IP]"
    # Had to change from sp.call to sp.Popen because of False positives
    ping = sp.Popen("ping -n {} -w {} {}".format(n_echos, wait, address),
                 stdout=sp.PIPE, stderr=sp.PIPE)  ## if you don't want it to print it out
    exit_code = ping.wait()

    return exit_code == 0


def ping_networks(host_address):
    unwanted_octets = [15, 56]
    network_addresses = ['192.168.1.', '192.168.2.']
    if host_address not in unwanted_octets:
        p = []
        for network_address in network_addresses:
            address = network_address + '%i' % host_address
            pi = ping(address)
            p.append(pi)
        if not all(pi == p[0] for pi in p):
            return host_address

if __name__ == "__main__":
    import time
    
    unmatched_octets = []
    unwanted_octets = [15, 56]
    network_addresses = ['192.168.1.', '192.168.2.']
    host_addresses = list(range(0,256))
    
    # If the system is CPU bound, use Pool (uses multiple processors)
    # If the system is I/O bound, use ThreadPool (uses multiple threads)
    # If unsure, just try both and see which one is slower
    # Same for ThreadPoolExecutor vs ProcessPoolExecutor
    from multiprocessing.pool import ThreadPool as Pool
    # from multiprocessing import Pool

    # Need to make a function that determines optimal number of threads
    pool_size = 100  # your "parallelness"

    # define worker function before a Pool is instantiated
    def worker(address):
        try:
            ping(network_address + '%i' % host_address)
        except:
            print('error with item')

    start_time = time.time()
    p = Pool(pool_size)
    unmatched_octets = p.map(ping_networks, host_addresses)
    # Without multithreading
    # for host_address in host_addresses:
            # ping_networks(network_adresses, host_adress)
    p.close()
    p.join()
    # to remove None values in list
    unmatched_octets = [i for i in unmatched_octets if i]
    print("Octets with different responses: ", unmatched_octets)
    print('Processing time: ', time.time() - start_time)
    # current_os = platform.system().lower()
    # if current_os == "windows":
        # parameter = "-n"
    # else:
        # parameter = "-c"

    # ip = "192.168.1.1"
    # exit_code = os.system(f"ping {parameter} 1 -w2 {ip} > /dev/null 2>&1")

    # print(exit_code == 0)


