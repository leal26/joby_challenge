#!/usr/bin/env python3
from unittest.mock import Mock
import unittest

from networking import address_checker

class TestSum(unittest.TestCase):

    def test_network_addresses(self):
        with self.assertRaises(TypeError):
            address_checker('192.168.1.')
            address_checker([])
            address_checker([1,2,3])
            address_checker(['192.168.1.'])
            address_checker(['500.168.1.', '192.168.2.'])
            address_checker(['192.1.'])
            address_checker(['192.1.2.23'])

    def test_host_addresses(self):
        network_addresses = ['500.168.1.', '192.168.2.']
        with self.assertRaises(TypeError):
            address_checker(network_addresses, host_addresses = '192.168.1.')
            address_checker(network_addresses, host_addresses = [])
            address_checker(network_addresses, host_addresses = [500])
            address_checker(network_addresses, host_addresses = [-1,-2,-3])
            address_checker(network_addresses, unwanted_addresses = '192.168.1.')
            address_checker(network_addresses, unwanted_addresses = [])
            address_checker(network_addresses, unwanted_addresses = [500])
            address_checker(network_addresses, unwanted_addresses = [-1,-2,-3])
            
    def test_integer_inputs(self):
        network_addresses = ['192.168.1.', '192.168.2.']
        with self.assertRaises(TypeError):
            address_checker(network_addresses, number_threads = '192.168.1.')
            address_checker(network_addresses, number_threads = [])
            address_checker(network_addresses, number_threads = -1)
            address_checker(network_addresses, n_echos = '192.168.1.')
            address_checker(network_addresses, n_echos = [])
            address_checker(network_addresses, n_echos = -1)
            address_checker(network_addresses, wait = '192.168.1.')
            address_checker(network_addresses, wait = [])
            address_checker(network_addresses, wait = -1)
            address_checker(network_addresses, n_attempts = '192.168.1.')
            address_checker(network_addresses, n_attempts = [])
            address_checker(network_addresses, n_attempts = -1)


    def test_ping(self):
        def side_effect(address):
            mock_values = {'192.168.1.0': 0, '192.168.2.0': 0,
                           '192.168.1.1': 0, '192.168.2.1': 1,
                           '192.168.1.2': 1, '192.168.2.2': 0,
                           '192.168.1.3': 1, '192.168.2.3': 1}
            return mock_values[address]
        
        network_addresses = ['192.168.1.', '192.168.2.']
        host_addresses = [0, 1, 2, 3]
        c = address_checker(network_addresses, host_addresses)

        # Sanity check if all all addresses are reached
        c.ping = Mock(return_value = 0)
        c.ping_all()
        self.assertEqual(len(c.unmatched_hosts), 0)

        # Sanity check if all all addresses are NOT reached
        c.ping.configure_mock(return_value = 1)
        c.ping_all()
        self.assertEqual(len(c.unmatched_hosts), 0)
        
        # Check case where only two pairs have unmatched responses
        c.ping = Mock(side_effect = side_effect)
        c.ping_all()
        self.assertEqual(len(c.unmatched_hosts), 2)
        self.assertEqual(c.unmatched_hosts, [1,2])

        # Check case where one of the unmatched responses host is unwanted
        c.host_unwanted = [0, 2]
        c.ping_all()
        self.assertEqual(len(c.unmatched_hosts), 1)
        self.assertEqual(c.unmatched_hosts, [1])
        
if __name__ == '__main__':
    unittest.main()