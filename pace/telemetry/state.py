"""
Handles setting up the Raspberry Pi for Monitoring
"""
import logging
import os
import threading

import pace.namespace as namespace


def monitor(adapter):
    """
    Place adapter in monitor mode
    :param adapter:
    :return:
    """
    logging.info("Issuing OS commands for monitor mode.")
    os.system('ifconfig ' + adapter + ' down')
    os.system('iwconfig ' + adapter + ' mode monitor')
    os.system('ifconfig ' + adapter + ' up')


def unmonitor(adapter):
    """
    Remove adapter from monitor mode
    :param adapter:
    :return:
    """
    logging.info("Recovering from monitor mode.")
    os.system('ifconfig ' + adapter + ' down')
    os.system('iwconfig ' + adapter + ' mode managed')
    os.system('ifconfig ' + adapter + ' up')


class Hopper:

    def __init__(self, device):
        self.device = device
        self.thread = None
        self.__stop = False

    def hop(self):
        """
        Enter a band hopping loop
        :return:
        """
        self.thread = threading.Thread(target=self.__hopper)
        self.thread.start()

    def __hopper(self):
        """
        Thread worker
        :return:
        """
        import time
        logging.info("Hopping channels.")
        while not self.__stop:
            os.system('iwconfig ' + self.device + ' channel 1')
            if not self.__stop:
                time.sleep(namespace.HOP_FREQUENCY)
            os.system('iwconfig ' + self.device + ' channel 6')
            if not self.__stop:
                time.sleep(namespace.HOP_FREQUENCY)
            os.system('iwconfig ' + self.device + ' channel 11')
            if not self.__stop:
                time.sleep(namespace.HOP_FREQUENCY)

    def stop(self):
        """
        Stop! Data time
        :return:
        """
        logging.info("Stopping channel hopper.")
        self.__stop = True
        self.thread = None
