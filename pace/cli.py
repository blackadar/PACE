"""
Coordinates the operation of a RasPi PACE machine
"""
import datetime
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

    # Initialize device
    state.monitor(namespace.ADAPTER)
    hopper = state.Hopper(namespace.ADAPTER)
    hopper.hop()

    # Collect Data
    area = congestion.Area(namespace.ADAPTER)
    area.monitor()

    # Register stopping tasks
    def signal_handler(sig, frame):
        print('Exiting PACE.')
        hopper.stop()
        area.stop()
        area.write()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        time.sleep(5)
        print_current(area.interval_total, area.interval_devices, area.last_interval, area.interval_ssids)


def print_current(tot: int, interval: set, last: datetime.datetime, ssids: dict):
    print("last dump: " + str(last))
    print("total probes: " + str(tot))
    print("mac pool: ")
    for item in interval:
        print(item)
    print("ssid requests: ")
    for key, val in ssids.items():
        print(str(key) + ": " + str(val))

    print("---------------------------")


def print_telemetry(telemetry: dict):
    for key, val in telemetry.items():
        print(key, val)
    print()


if __name__ == "__main__":
    main()
