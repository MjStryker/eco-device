
import os
from random import randint
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

    # if(gce_index_jour > 0):
    file_manager.add_indexes(
        datetime.now(), gce_index_jour, gce_index_total)


def wait_until_specific_time():
    run = True
    while run:
        now = datetime.now()
        if(now.second % config.delay == 0):
            break
        # print("Not now...")
        time.sleep(.5)


def loop():
    i = 0
    start_time = time.time()
    while True:
        wait_until_specific_time()
        now = datetime.now()
        print("{} - Executing job #{}".format(now.strftime("%X"), i+1))
        job(i)
        print()
        time.sleep(config.delay - ((time.time() - start_time) % config.delay))
        i += 1


if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
