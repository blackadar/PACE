"""
Coordinates the operation of a RasPi PACE machine
"""
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

    while True:
        area.write()
        time.sleep(10)
        print(area.devices)


if __name__ == "__main__":
    main()
