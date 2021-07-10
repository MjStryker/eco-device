
import os
import sys
import time

from datetime import datetime

import gce.devices.water as gce

import file_manager


def job():
    gce_index_jour, gce_index_total = gce.get_water_indexes()
    print(" Index jour :", gce_index_jour, "\nIndex total :", gce_index_total)


def loop():
    i = 1
    while True:
        now = datetime.now()
        print("{} - Executing job #{}".format(now.strftime("%X"), i))
        job()
        i += 1
        time.sleep(5)


if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
