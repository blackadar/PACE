"""
Namespace Variables
Intended to define constants.
"""
import os

# Interpretation Parameters
RECENT_PERSIST = 15  # Time in minutes to consider a device as already present

# File I/O
INSTALL_PATH = os.path.dirname(os.path.realpath(__file__))  # Path to Python code
DATA_PATH = 'data/'  # Path to general data output
DATA_WRITE = 1  # Time interval in minutes to write dataframe to a file

# Device Properties
ADAPTER = 'wlan1'  # Monitor mode adapter iface name

# Sniffing Parameters
HOP_FREQUENCY = 2  # Seconds between channel hops
FRAME_INTERVAL = 60 * 10  # Seconds between set separation
