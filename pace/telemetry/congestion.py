"""
Packet Processing -> Congestion Data
Spooky code ahead
"""
import datetime
import pickle
import threading
import time

from scapy.all import Dot11, sniff

import pace.namespace as namespace


class Area:

    def __init__(self, interface):
        """
        Initialize an Area with defaults
        """
        self.last_interval = datetime.datetime.now()
        self.interval_devices = set()  # Safe to ignore duplicates within interval
        self.interval_ssids = {}
        self.interval_total = 0
        self.interface = interface
        self.interval_thread = None
        self.sniff_thread = None
        self.__stop = threading.Event()

    def register(self, mac, info):
        """
        Registers a MAC as seen in the area
        :param mac:
        :return:
        """
        self.interval_total += 1
        self.interval_devices.add(mac)
        if info != '':
            if info not in self.interval_ssids.keys():
                self.interval_ssids[info] = 1
            else:
                self.interval_ssids[info] += 1

    def new_interval(self):
        """
        Remove old entries
        :return:
        """
        self.interval_devices = set()
        self.interval_ssids = {}
        self.interval_total = 0
        self.last_interval = datetime.datetime.now()

    def monitor(self):
        """
        Start sniffing the area in a separate thread
        :return:
        """
        self.__stop.clear()
        self.sniff_thread = threading.Thread(target=self.__monitor_worker)
        self.sniff_thread.start()
        self.interval_thread = threading.Thread(target=self.__interval_worker)
        self.interval_thread.start()

    def __interval_worker(self):
        """
        Every FRAME_INTERVAL seconds, append the device set to the dictionary and clear it.
        :return:
        """
        while not self.__should_stop(None):
            time.sleep(namespace.FRAME_INTERVAL)
            self.write()
            self.new_interval()

    def __monitor_worker(self):
        """
        I'm a fool to do your dirty work
        Oh yeah
        :return:
        """
        sniff(iface=self.interface, prn=self.handle_event, stop_filter=self.__should_stop)

    def __should_stop(self, garbage):
        """
        Returns True if the sniffer should stop, instead of reading next packet.
        :return:
        """
        return self.__stop.is_set()

    def stop(self):
        """
        Stop the monitor thread, if it exists
        :return:
        """
        self.__stop.set()

    def handle_event(self, pkt):
        """
            Handle a packet from scapy
            I-Spy some useful data
            :param pkt: Packet from sniffer
            :return:
            """
        if not pkt.haslayer(Dot11):
            return  # Don't care
        if pkt.type == 0 and pkt.subtype == 4:  # IEEE 802.11 Management, Re-Association Request
            curmac = pkt.addr2
            curmac = curmac.upper()
            self.register(curmac, pkt.info.decode('ascii'))

    def write(self):
        """
        Write telemetry to file
        :return:
        """
        telemetry = {'Interval': self.last_interval, 'Devices': self.interval_devices,
                     'Total Probes': self.interval_total, 'SSID Requests': self.interval_ssids}
        import pace.analysis.read
        pace.analysis.read.check_create_data()
        with open(namespace.DATA_PATH + time.strftime("%Y%m%d_%H%M%S.pkl"), "wb") as pkl:
            pickle.dump(telemetry, pkl)
