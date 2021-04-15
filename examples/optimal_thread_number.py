from networking import address_checker


## Inputs
# Network addresses (first three octets) to evalaute
network_addresses = ['192.168.1.', '192.168.2.']
# number of attemps in case an address is not responsive
n_attempts = 2

# Define object with all inputs
c = address_checker(network_addresses, n_attempts=n_attempts)

# Find out optimal number of threads for your computer
optimal_runtime, optimal_threads = c.optimal_thread_number(plot=True)
print("Optimal runtime: ", optimal_runtime)
print('Optimal number of threads: ', optimal_threads)
