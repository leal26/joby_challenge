import platform    # For getting the operating system name
import subprocess as sp  # For executing a shell command
import threading
import time
import os

class address_checker():
    def __init__(self, network_addresses, host_addresses = list(range(256)),
                 host_unwanted = [], pool_size=100, n_echos = 1, wait = 2,
                 n_retries=2):
        
        # Assign properties
        self.network_addresses = network_addresses
        self.host_addresses = host_addresses
        self.host_unwanted = host_unwanted
        self.pool_size = pool_size
        self.n_retries = n_retries
        self.n_echos = n_echos
        self.wait = wait
        
        self._check_inputs()

    def _check_inputs(self):
        '''Evaluates if inputs are the correct format. This is evaluated when
           object is created and before any major operation (ping multiple addresses)
           just in case the user changed the variables.'''
           
        # Check if OS is Windows. It should run for Linux, but was not tested
        if platform.system().lower() != 'windows':
            raise TypeError('This library has not been verified for non-Windows OS')
        
        # Check if all list inputs are properly formmated
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
        for name in ['pool_size', 'n_echos', 'n_retries']:
            values = getattr(self, name)
            
            if not isinstance((values), (int) ):
                raise TypeError(name + " should be an integer")
            

    def show(self):
        attrs = vars(self)
        print(''.join("%s: %s\n" % item for item in attrs.items()))
        
    def ping(address, n_echos = 1, wait=10):
        """
        Only tested for Windows and IPv4 address/
        
        Returns True if address (str) responds to a ping request.
        Inputs:
        - n_echos: Specifies the number of echo Request messages be sent. The default is 1.
        - wait: Specifies the amount of time, in milliseconds, to wait for the echo.
        Windows Ping doc: https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/ping
        """

        # Option for the number of packets as a function of OS
        if platform.system().lower()=='windows':
            param = '-n' 
        else:
            param = '-c'
        
        # Building the command. Ex: "ping -n 2 -w 2 [IP]" (sp.call returns False positives)
        ping = sp.Popen("ping -n {} -w {} {}".format(n_echos, wait, address),
                     stdout=sp.PIPE, stderr=sp.PIPE)

        # If adress responds, exit_code is 0
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

 


