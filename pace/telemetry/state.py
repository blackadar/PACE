"""
Handles setting up the Raspberry Pi for Monitoring
"""
import subprocess
import threading


def monitor(adapter):
    """
    Place adapter in monitor mode
    :param adapter:
    :return:
    """
    subprocess.call(['ifconfig', adapter, 'down'])
    subprocess.call(['iwconfig', adapter, 'mode monitor'])


def unmonitor(adapter):
    """
    Remove adapter from monitor mode
    :param adapter:
    :return:
    """
    subprocess.call(['ifconfig', adapter, 'up'])


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
        while not self.__stop:
            subprocess.call('iwconfig', self.device, 'channel 1')
            if not self.__stop:
                time.sleep(3)
            subprocess.call('iwconfig', self.device, 'channel 6')
            if not self.__stop:
                time.sleep(3)
            subprocess.call('iwconfig', self.device, 'channel 11')
            if not self.__stop:
                time.sleep(3)

    def stop(self):
        """
        Stop! Data time
        :return:
        """
        self.__stop = True
        self.thread = None
