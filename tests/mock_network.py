from unittest.mock import Mock
from networking import address_checker


host_unwanted = [15, 56]
network_addresses = ['192.168.1.', '192.168.2.']
host_addresses = list(range(0,256))
number_threads = 130

c = address_checker(network_addresses)

c.ping = Mock()
c.ping.return_value = 0
c.ping_all()
assert len(c.unmatched_hosts) == 0

c.ping = Mock()
c.ping.return_value = 1
c.ping_all()
assert len(c.unmatched_hosts) == 0

# print("Host addresses with different responses: ", c.unmatched_hosts)
# print('Processing time: ', c.runtime)

c.optimal_thread_number()