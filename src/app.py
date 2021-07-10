
import os
import sys
import time

from datetime import datetime

import gce.devices.water as gce

import dev
import file_manager
import config


def job(step: int):
    # gce_index_jour, gce_index_total = gce.get_water_indexes()
    # print(" Index jour :", gce_index_jour, "\nIndex total :", gce_index_total)
    gce_index_jour, gce_index_total = dev.generate_random_entry(
        config.Device_type.WATER, step)
    file_manager.add_indexes(
        datetime.now(), gce_index_jour, gce_index_total)


def loop():
    i = 0
    while True:
        now = datetime.now()
        print("{} - Executing job #{}".format(now.strftime("%X"), i+1))
        job(i)
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
