
import config
import gce.devices.water as gce

from datetime import datetime

import os
import sys
import time

if __name__ == "__main__":
    print(gce.get_water_info())
    # water_daily_consumption, water_counter_index = gce.get_water_indexes()
    # print("{now} - {water_daily_consumption} - {water_counter_index}".format(now=datetime.now().strftime("%Y-%m-%d %X"),
    #                                                                          water_daily_consumption=water_daily_consumption, water_counter_index=water_counter_index))
