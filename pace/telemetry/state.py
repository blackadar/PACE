"""
Handles setting up the Raspberry Pi for Monitoring
"""
import subprocess


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


def hop():
    """
    Enter a band hopping loop
    :return:
    """
    pass
