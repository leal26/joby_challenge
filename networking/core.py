#!/usr/bin/env python3
from multiprocessing.pool import ThreadPool as Pool
import matplotlib.pyplot as plt
import subprocess as sp 
import threading 
import platform    
import time
import os

class address_checker():
    """This is a class to evaluate responsativity of multiple addresses to a ping 
       and find addresses with same host but different networks addresses that have
       different responses to a ping.

    Inputs
    ----------
    :param network_addresses
    :type network_addresses: list
    
    :param host_addresses: a list of integers containing all host addresses, defaults to [0, ..., 255]
    :type host_addresses: list, optional
    
    :param host_unwanted: ,defaults to []
    :type host_unwanted: list, optional
    
    :param number_threads: , defaults to 130
    :type number_threads: int, optional
    
    :param n_echos: specifies the number of echo Request messages be sent, defaults to 1
    :type n_echos: int, optional
    
    :param wait: specifies the amount of time, in milliseconds, to wait for the echo, defaults to 2 ms
    :type wait: int, optional
    
    :param n_attempts: , defaults to 2
    :type n_attempts: int, optional

    See Also
    --------
    empty_like, zeros

    Examples
    --------
    >>> import numpy.matlib
    >>> np.matlib.empty((2, 2))    # filled with random data
    matrix([[  6.76425276e-320,   9.79033856e-307], # random
            [  7.39337286e-309,   3.22135945e-309]])
    >>> np.matlib.empty((2, 2), dtype=int)
    matrix([[ 6600475,        0], # random
            [ 6586976, 22740995]])

    """
    def __init__(self, network_addresses, host_addresses = list(range(256)),
                 host_unwanted = [], number_threads=130, n_echos = 1, wait = 2,
                 n_attempts=2):
   
        """Constructor method
        """
        # Assign properties
        self.network_addresses = network_addresses
        self.host_addresses = host_addresses
        self.host_unwanted = host_unwanted
        self.number_threads = number_threads
        self.n_attempts = n_attempts
        self.n_echos = n_echos
        self.wait = wait
        
        # Option for the number of packets as a function of OS
        if platform.system().lower()=='windows':
            self.param = '-n' 
        else:
            self.param = '-c'

        # Check if inputs are properly formatted
        self._check_inputs()

    def _check_inputs(self):
        '''Evaluates if inputs are the correct format. This is evaluated when
           object is created and before any major operation (ping multiple addresses)
           just in case the user changed the variables.
        '''
           
        # Check if OS is Windows. It should run for Linux, but was not tested
        if platform.system().lower() != 'windows':
            raise TypeError('This library has not been verified for non-Windows OS')
        
        # Check if all list inputs are properly formatted
        for name in ['network_addresses', 'host_addresses', 'host_unwanted']:
            values = getattr(self, name)
            
            # Check if inputs are lists
            if not isinstance((values), (list, tuple) ):
                raise TypeError(name + " should be an indexable format such as a list")

            # Check for empty lists
            if name in ['network_addresses', 'host_addresses']:
                if len((values)) == 0:
                    raise TypeError(name + " should not be empty")
                
            if name == 'network_addresses':
                # At least two network addresses should be provided
                if len(values) < 2:
                        raise TypeError(name + " should have at least two network addresses.")
                        
                for value in values:
                    # network_addresses should consist only of strings 
                    if not isinstance(value, (str) ):
                        raise TypeError(name + " should consists of strings such as '192.168.1.'")
                        
                    split_value = value.split('.')
                    # network_addresses should follow a quad-dotted address
                    if len(split_value) != 4:
                        raise TypeError(name + " should be a quad-dotted address such as '192.168.1.'")
                        
                    # the host address for the IP in network_addresses should be missing
                    if split_value[-1] != '':
                        raise TypeError(name + " should be missing the last octet of IP")
                        
                    # Each octet should be less than 256
                    if not all( int(octate) < 256 for octate in split_value[:-1]):
                        raise TypeError("Each octet should be lower than 256")
                        
            # host_addresses and host_unwanted should consists only of integers
            else:
                if not all (isinstance(value, (int) ) for value in values):
                    if not all ((value >= 0 and value < 256) for value in values):
                        raise TypeError(name + "should consists of positive integers lower than 256")

        # Check if all list inputs are properly formmated
        for name in ['number_threads', 'n_echos', 'n_attempts']:
            values = getattr(self, name)
            
            if not isinstance((values), (int) ):
                raise TypeError(name + " should be an integer")
                
            if values < 1:
                raise TypeError(name + " should be an integer equal to or more than one")

    def show(self):
        attrs = vars(self)
        print(''.join("%s: %s\n" % item for item in attrs.items()))
        
    def ping(self, address):
        """Pings address. Returns True if an echo is received.
        Inputs
        ----------
        :param address: a string in dot-decimal notation is expected
        :type address: string

        Notes
        ----------
        Windows ping doc: https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/ping
        """
        self._check_inputs()
        
        exit_code = False
        attempts = 0
        
        while attempts < self.n_attempts and not exit_code:
            # Building the command. Ex: "ping -n 2 -w 2 [IP]" (sp.call returns False positives)
            ping = sp.Popen("ping {} {} -w {} {}".format(self.param, self.n_echos, self.wait, address),
                         stdout=sp.PIPE, stderr=sp.PIPE)

            # If adress responds, exit_code is True
            exit_code = ping.wait() == 0
            attempts += 1

        return exit_code


    def ping_networks(self, host_address):

        if host_address not in self.host_unwanted:
            p = []
            for network_address in self.network_addresses:
                address = network_address + '%i' % host_address
                pi = self.ping(address)
                p.append(pi)

            if not all(pi == p[0] for pi in p):
                return host_address

    def ping_all(self, runtime = False):
        '''pings all addresses for all networks
        
        Inputs (optional):
            - runtime: if True, will calculate how long it took to run (default is False)
        '''
            
        self._check_inputs()
        
        # Keep track of time
        if runtime: start_time = time.time()
        
        # Ping utilizing multithreading
        p = Pool(self.number_threads)
        unmatched_hosts = p.map(self.ping_networks, self.host_addresses)
        p.close()
        p.join()
        
        # Networks addresses with same ping results return None. So we remove them 
        self.unmatched_hosts = [i for i in unmatched_hosts if i]
        
        # Find out time run
        if runtime: self.runtime = time.time() - start_time

    def optimal_thread_number(self, thread_range=list(range(10, 210, 10)), plot=False):
        """Determines .
        Inputs
        ----------
        :param address: a string in dot-decimal notation is expected
        :type address: string

        Returns
        -------
    
        Notes
        ----------
        Windows ping doc: https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/ping
        """
        runtimes = []
        for self.number_threads in thread_range:
            self.ping_all(runtime=True)
            runtimes.append(self.runtime)

        if plot:
            plt.figure()
            plt.plot(thread_range, runtimes)
            plt.xlabel('Number of threads')
            plt.ylabel('Runtime (s)')
            plt.show()
            
        optimal_runtime = min(runtimes)
        return optimal_runtime, (thread_range[runtimes.index(optimal_runtime)])