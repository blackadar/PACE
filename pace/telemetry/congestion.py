"""
Packet Processing -> Congestion Data
Spooky code ahead
"""
import datetime

from scapy.all import Dot11


class Area:

    def __init__(self):
        """
        Initialize an Area with defaults
        """
        self.devices = {}

    def register(self, mac):
        """
        Registers a MAC as seen in the area
        :param mac:
        :return:
        """
        if mac not in self.devices.keys():
            self.devices[mac] = [datetime.datetime.now(), ]
        else:
            self.devices[mac].append(datetime.datetime.now())

    def clean(self):
        """
        Remove old entries
        :return:
        """
        self.devices = {}

    def write(self, path):
        """
        Write telemetry to file
        :param path:
        :return:
        """
        # TODO: FILE I/O
        # First check if a file exists. If so, read in the existing dictionary
        # If no contents, make a new file and write the dick
        # If contents exist, append the dictionary (KEEPING KEYS!) and write it out
        # In whatever the user is in, check if exists/create a pickle spot


def handle_packet(pkt, area: Area):
    """
    Handle a packet from scapy
    I-Spy some useful data
    :param pkt:
    :param area:
    :return:
    """
    if not pkt.haslayer(Dot11):
        return  # Don't care
    if pkt.type == 0 and pkt.subtype == 4:  # Look only for Probe Requests
        curmac = pkt.addr2
        curmac = curmac.upper()
        area.register(curmac)
