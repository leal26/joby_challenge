.. Joby Challenge documentation master file, created by
   sphinx-quickstart on Wed Apr 14 14:42:08 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Joby Challenge: Networking
==========================================

This is a library intended:

* to evaluate responsativity of multiple addresses to a ping
  
* find addresses with same host (last octet) but different networks addresses
  (first three octets) that have different ping responses.

This library has only been tested on Windows OS. Accomodations are made for
Linux based systems, but performance is not guaranteed.

       
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   documentation


Examples
==================

For convenience, the dot-decimal representation of an IPv4 address 
(e.g., 192.168.1.134) is broken down to:

* the 'network address' consisting of the first three octets of the address
  (e.g., 192.168.1.), and
  
* the 'host address' that is the last octet of the address(e.g., 134).

The main use of the API is provided below where a user wants to find the host
addresses that have different ping responses for all network addresses in
``network_addresses``. All host addresses are evaluated (0 to 255)
except for those defined in ``host_unwanted``. ``n_attempts`` attempts are done
for every IPv4 address is not until an echo is received.

.. code-block:: python

    import address_checker from networking
    host_unwanted = [15, 56]
    network_addresses = ['192.168.1.', '192.168.2.']
    n_attempts = 3
    c = address_checker(network_addresses, n_echos=n_echos,
                        n_attempts=n_attempts)
    c.ping_all()
    

The number of threads that leads to the fastest execution of ``c.ping_all()`` 
depends on the users's platform. Therefore, if optimal performance is desired, 
the optimal number of threads can be calculated with ``c.optimal_thread_number()``

.. code-block:: python

    import address_checker from networking
    network_addresses = ['192.168.1.', '192.168.2.', '192.168.4.']
    c = address_checker(network_addresses, n_echos=n_echos)
    optimal_runtime, optimal_threads = c.optimal_thread_number(plot=True)
    
