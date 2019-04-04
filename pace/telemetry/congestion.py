"""
Packet Processing -> Congestion Data
Spooky code ahead
"""
import datetime
import logging
import pickle
import threading
import time

from scapy.all import Dot11, sniff

import pace.analysis.read
import pace.namespace as namespace


class Area:

    def __init__(self, interface):
        """
        Initialize an Area with defaults
        """
        logging.info("Initializing Area on interface " + str(interface))
        self.last_interval = datetime.datetime.now()
        self.interval_devices = set()  # Safe to ignore duplicates within interval
        self.interval_ssids = {}
        self.interval_devices_lock = threading.RLock()
        self.interval_ssids_lock = threading.RLock()
        self.interval_total = 0
        self.interface = interface
        self.interval_thread = None
        self.sniff_thread = None
        self.__stop = threading.Event()

    def register(self, mac, info):
        """
        Registers a MAC as seen in the area
        :param info:
        :param mac:
        :return:
        """
        self.interval_total += 1
        with self.interval_devices_lock:
            self.interval_devices.add(mac)
        if info != '':
            with self.interval_ssids_lock:
                if info not in self.interval_ssids.keys():
                    self.interval_ssids[info] = 1
                else:
                    self.interval_ssids[info] += 1

    def new_interval(self):
        """
        Remove old entries
        :return:
        """
        with self.interval_devices_lock and self.interval_ssids_lock:
            # Attempt to prevent memory leak
            del self.interval_devices
            del self.interval_ssids
            del self.interval_total
            del self.last_interval

            self.interval_devices = set()
            self.interval_ssids = {}
            self.interval_total = 0
            self.last_interval = datetime.datetime.now()
            logging.debug("Starting a new time frame at " + str(self.last_interval))

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
            for i in range(namespace.FRAME_INTERVAL):
                time.sleep(1)
            self.write()
            self.new_interval()

    def __monitor_worker(self):
        """
        I'm a fool to do your dirty work
        Oh yeah
        :return:
        """
        logging.debug("Initializing Scapy on " + str(self.interface))
        sniff(iface=self.interface, prn=self.handle_event, stop_filter=self.__should_stop, store=0)

    def __should_stop(self, __):
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
        logging.debug("Stopping Area threads.")
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
            ssid = ''
            try:
                ssid = pkt.info.decode('utf-8')
            except:
                logging.debug("Couldn't decode a strange ssid: " + str(pkt.info))
            self.register(curmac, ssid)

    def write(self):
        """
        Write telemetry to file
        :return:
        """
        name = namespace.DATA_PATH + time.strftime("%Y%m%d_%H%M%S.pkl")
        logging.debug("Writing to file " + name)
        with self.interval_devices_lock and self.interval_ssids_lock:
            telemetry = {'Interval': self.last_interval, 'Devices': self.interval_devices,
                         'Total Probes': self.interval_total, 'SSID Requests': self.interval_ssids}
        pace.analysis.read.check_create_data()
        with open(name, "wb") as pkl:
            pickle.dump(telemetry, pkl)

    def log(self):

        logging.debug("last dump: " + str(self.last_interval))
        logging.debug("total probes: " + str(self.interval_total))
        logging.debug("mac pool: ")
        with self.interval_devices_lock:
            for item in self.interval_devices:
                logging.debug(" " + item)
        logging.debug("ssid requests: ")
        with self.interval_ssids_lock:
            for key, val in self.interval_ssids.items():
                logging.debug(" " + str(key) + ": " + str(val))

        logging.debug("---------------------------")
