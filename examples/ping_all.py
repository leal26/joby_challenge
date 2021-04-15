from networking import address_checker

## Inputs
# Undesirable host addresses
host_unwanted = [15, 56]
# Network addresses (first three octets) to evalaute
network_addresses = ['192.168.1.', '192.168.2.']
# number of attemps in case an address is not responsive
n_attempts = 2

# Define object with all inputs
c = address_checker(network_addresses, host_unwanted=host_unwanted,
                    n_attempts=n_attempts)

# Print configuration to double check everything
# c.show()

# Ping one address
# print(c.ping('192.168.2.149'))

# Ping all host addresses for all network addresses
c.ping_all()
print("Host addresses with different responses: ", c.unmatched_hosts)
