# Joby Challenge: networking
This is library intended to ping addresses in a network and find addresses
that share the same host address (last octet) but have have different responses
to the ping command.

This library has only been tested on Windows OS. Accomodations are made for
Linux based systems, but performance is not guaranteed.

# Installation
- Clone via GitHub
- Open command line in aeropy directory
- Run 'pip install -e .'
- cd tests
- python -m unittest
- If all tests pass, the library is properly installed

# Dependencies
There are no dependencies that do not already come installed with Python
- multiprocessing
- matplotlib
- subprocess
- platform
- time
- os