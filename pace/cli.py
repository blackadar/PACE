"""
Coordinates the operation of a RasPi PACE machine
"""
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
    logging.basicConfig(filename='pace.log', level=logging.INFO, format='%(asctime)s %(levelname)s:  %(message)s')

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error("Uncaught Exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception

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
        area.log()


if __name__ == "__main__":
    main()
