
import os
import sys
import time

from datetime import datetime

import gce.devices.water as gce

import dev
import file_manager
import config

env = "dev"


def job():
    now = datetime.now()
    job_nb = file_manager.get_file_nb_lines(now) + 1

    if(env == "prod"):
        gce_index_jour, gce_index_total = gce.get_water_indexes()
        print(" Index jour :", gce_index_jour,
              "\nIndex total :", gce_index_total)

    elif(env == "dev"):
        gce_index_jour, gce_index_total = dev.generate_random_entry(
            config.Device_type.WATER)

    addedvalue = " (+{})".format(gce_index_jour) if gce_index_jour > 0 else ""
    step_str_format = "[ {} / {} ] ".format(job_nb, config.nb_of_steps_per_day)

    print(step_str_format + datetime.now().strftime("%Y-%m-%d %X") +
          " -> " + str(gce_index_total) + addedvalue)

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
    start_time = time.time()
    while True:
        wait_until_specific_time()
        # print("{} - Executing job #{}".format(now.strftime("%X"), job_nb+1))

        job()

        # print()

        time.sleep(config.delay - ((time.time() - start_time) % config.delay))


if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
