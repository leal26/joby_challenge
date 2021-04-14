from networking import address_checker


host_unwanted = [15, 56]
network_addresses = ['192.168.1.', '192.168.2.']
host_addresses = list(range(0, 256))
n_echos = 1

c = address_checker(network_addresses, n_echos=n_echos)

# Find out optimal number of threads for your computer
optimal_runtime, optimal_threads = optimal_thread_number(plot=True)
print("Optimal runtime: ", optimal_runtime)
print('Optimal number of threads: ', optimal_threads)
