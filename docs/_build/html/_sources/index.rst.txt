.. Joby Challenge documentation master file, created by
   sphinx-quickstart on Wed Apr 14 14:42:08 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Joby Challenge: Networking
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   documentation

Examples
==================

An object for the class 'address_checker' needs to be defined for every script.
The first three octets of the dot-decimal address is denoted as 
'network_address' (e.g., 192.168.1.), and the last octed is denoted as
host_address'.  

.. code-block:: python

    import address_checker from networking
    host_unwanted = [15, 56]
    network_addresses = ['192.168.1.', '192.168.2.']
    n_attempts
    c = address_checker(network_addresses, n_echos=n_echos,
                        n_attempts=n_attempts)
    c.ping_all()
    
The number of threads that leads to the fastest execution of 'c.ping_all()' 
depends on the users's platform. Therefore, if optimal performance is desired, 
the optimal number of threads can be calculated with c.optimal_thread_number()

.. code-block:: python

    import address_checker from networking
    network_addresses = ['192.168.1.', '192.168.2.', '192.168.4.']
    c = address_checker(network_addresses, n_echos=n_echos)
    optimal_runtime, optimal_threads = c.optimal_thread_number(plot=True)
    
