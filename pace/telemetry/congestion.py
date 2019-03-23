"""
Packet Processing -> Congestion Data
Spooky code ahead
"""
from scapy.all import Dot11


class Area:

    def __init__(self):
        self.recent = set()  # Devices seen within the past n minutes

    def register(self, mac):
        if mac in self.recent:
            pass
        else:
            self.recent.add(mac)


def handle_packet(pkt, area: Area):
    if not pkt.haslayer(Dot11):
        return  # Don't care
    if pkt.type == 0 and pkt.subtype == 4:  # Look only for Probe Requests
        curmac = pkt.addr2
        curmac = curmac.upper()
        area.register(curmac)
