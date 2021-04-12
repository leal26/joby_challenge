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
        network_addresses = ['500.168.1.', '192.168.2.']
        with self.assertRaises(TypeError):
            address_checker(network_addresses, pool_size = '192.168.1.')
            address_checker(network_addresses, pool_size = [])
            address_checker(network_addresses, pool_size = -1)
            address_checker(network_addresses, n_echos = '192.168.1.')
            address_checker(network_addresses, n_echos = [])
            address_checker(network_addresses, n_echos = -1)
            address_checker(network_addresses, wait = '192.168.1.')
            address_checker(network_addresses, wait = [])
            address_checker(network_addresses, wait = -1)
            address_checker(network_addresses, pool_size = '192.168.1.')
            address_checker(network_addresses, pool_size = [])
            address_checker(network_addresses, pool_size = -1)
            
            
if __name__ == '__main__':
    unittest.main()