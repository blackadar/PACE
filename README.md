# Public Area Congestion Evaluator (P.A.C.E.) #

This library is intended for deployment to low-energy computers in public areas to evaluate the number of people present in the area over time.
With an attached network card capable of running in monitor mode, the tool will collect the MAC hardware addresses of the devices in the area,
and present this data to the hub server for in-depth analysis. One or many spoke devices can be used to present multiple sets to the user.

# Intended Uses

This product is useful in a variety of situations, however public locations such as libraries, office spaces, and retail locations will see immediate benefits
to the analysis of traffic flow through their locations.

# Contributing

It is critical to organize all contributions into the existing structure to maintain a clean codebase.
Ensure all contributions conform to PEP-8.

# Running the Software
On a Raspberry Pi, pull a recent copy of the library. Modify the namespace to your device's adapter name.
Run the command `sudo -b nohup python3 -m pace.cli` so that the tool can run in the background.
To monitor the log, use `tail -f pace.log`.