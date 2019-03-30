"""
Coordinates the operation of a RasPi PACE machine
"""
import datetime
import logging
import signal
import sys
import time

import pace.namespace as namespace
import pace.telemetry.congestion as congestion
import pace.telemetry.state as state


def main():
    """
    Let's do this thing!
    :return:
    """

    # Start the Logger
    logging.basicConfig(filename='pace.log', level=logging.DEBUG, format='%(levelname)s:  %(message)s')

    # Initialize device
    state.monitor(namespace.ADAPTER)
    hopper = state.Hopper(namespace.ADAPTER)
    hopper.hop()

    # Collect Data
    area = congestion.Area(namespace.ADAPTER)
    area.monitor()

    # Register stopping tasks
    def signal_handler(sig, frame):
        logging.info('Caught SIGINT, exiting..')
        hopper.stop()
        area.stop()
        area.write()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        time.sleep(5)
        print_current(area.interval_total, area.interval_devices, area.last_interval, area.interval_ssids)


def print_current(tot: int, interval: set, last: datetime.datetime, ssids: dict):
    logging.debug("last dump: " + str(last))
    logging.debug("total probes: " + str(tot))
    logging.debug("mac pool: ")
    for item in interval:
        logging.debug(" " + item)
    logging.debug("ssid requests: ")
    for key, val in ssids.items():
        logging.debug(" " + str(key) + ": " + str(val))

    logging.debug("---------------------------")


def print_telemetry(telemetry: dict):
    for key, val in telemetry.items():
        print(key, val)
    print()


if __name__ == "__main__":
    main()
