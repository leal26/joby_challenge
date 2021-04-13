from networking import address_checker


host_unwanted = [15, 56]
network_addresses = ['192.168.1.', '192.168.2.']
host_addresses = list(range(0,256))
n_echos = 1

c = address_checker(network_addresses, n_echos=n_echos)
c.show()

# print(c.ping('192.168.2.149'))
# print(c.ping_networks(149))
c.ping_all(runtime=True)

print("Host addresses with different responses: ", c.unmatched_hosts)
print('Processing time: ', c.runtime)

# c.optimal_thread_number()