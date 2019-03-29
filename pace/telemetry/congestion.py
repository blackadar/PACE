"""
Packet Processing -> Congestion Data
Spooky code ahead
"""
import datetime
import pickle

from scapy.all import Dot11

import pace.namespace as namespace


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
            self.devices[mac] = {datetime.datetime.now(), }
        else:
            self.devices[mac].add(datetime.datetime.now())

    def clean(self):
        """
        Remove old entries
        :return:
        """
        self.devices = {}

    def write(self):
        """
        Write telemetry to file
        :return:
        """
        import pace.analysis.read as rd
        rd.check_create_data()
        if not rd.data_exists(namespace.DATA_PATH):
            with open(namespace.PICKLE, "wb") as pkl:
                pickle.dump(self.devices, pkl)
        else:
            with open(namespace.PICKLE, "rb") as pkl:
                total_telemetry = pickle.load(pkl)
            t_keys = total_telemetry.keys()
            for mac in self.devices.keys():
                if mac in t_keys:
                    total_telemetry[mac].update(self.devices[mac])
                else:
                    total_telemetry[mac] = self.devices[mac]
            # TODO: Delete existing pickle file
            # TODO: Write total_telemetry to pickle file


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
