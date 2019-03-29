"""
Namespace Variables
Intended to define constants.
"""
import os

# Interpretation Parameters
RECENT_PERSIST = 15  # Time in minutes to consider a device as already present
DATA_WRITE = 1  # Time interval in minutes to write dataframe to a file

# File I/O
INSTALL_PATH = os.path.dirname(os.path.realpath(__file__))
PICKLE = 'data/telemetry.pkl'
