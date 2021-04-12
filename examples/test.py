from networking import address_checker


host_unwanted = [15, 56]
network_addresses = ['192.168.1.', '192.168.2.']
host_addresses = list(range(0,256))
pool_size = 100

c = address_checker(network_addresses)
c.show()