"""
Packet Processing -> Congestion Data
Spooky code ahead
"""
from scapy.all import Dot11


class Area:

    def __init__(self):
        """
        Initialize an Area with defaults
        """
        self.recent = set()  # Devices seen within the past n minutes
        self.congestion = -1.0

    def register(self, mac):
        """
        Registers a MAC as seen in the area
        :param mac:
        :return:
        """
        if mac in self.recent:
            pass
        else:
            self.recent.add(mac)

    def clean(self):
        """
        Remove old entries
        :return:
        """
        self.recent = set()

    def write(self, path):
        """
        Write telemetry to file
        :param path:
        :return:
        """
        pass


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
