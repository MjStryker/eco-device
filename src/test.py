import os
import sys
import time

import config
# import gce.devices.water as gce

from datetime import datetime, timedelta
from random import randint, shuffle


daily_water_consumption_avg = 330

daily_water_consumption_in_percentage = (1.5, 0.5, 0.5, 0.5, 1.0, 2.0, 2.5, 4.0,
                                         6.0, 7.0, 6.0, 7.0, 6.0, 5.5, 4.0, 2.0, 6.0, 7.5, 8.0, 7.5, 5.5, 5.5, 2.5, 1.5)


def get_hourly_random_water_usage(current_hour_max):
    nb_of_step_per_hour = int(3600/config.delay)

    steps_per_hour = [0 for i in range(nb_of_step_per_hour)]

    total_hourly_random_water_usage = 0
    for step in range(nb_of_step_per_hour):
        random_value = randint(1, 3)
        res = random_value if (total_hourly_random_water_usage + random_value <=
                               current_hour_max) else 0
        total_hourly_random_water_usage += res
        steps_per_hour[step] = res

    shuffle(steps_per_hour)
    return steps_per_hour


def get_daily_random_water_usage():
    daily_water_usage = [-1 for i in range(24)]
    total_daily_random_water_usage = 0

    for hour in range(24):
        condition_for_more_water_usage = randint(0, 3) == 0
        delta = randint(1, 8) if condition_for_more_water_usage else 0
        hourly_percentage = daily_water_consumption_in_percentage[hour]
        current_hour_max = int(daily_water_consumption_avg *
                               hourly_percentage / 100 + delta)
        hourly_random_water_usage = get_hourly_random_water_usage(
            current_hour_max)
        daily_water_usage[hour] = hourly_random_water_usage
        total_daily_random_water_usage += current_hour_max

    return daily_water_usage


if __name__ == "__main__":
    # today = datetime.now().strftime("%Y-%m-%d")
    # yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    # print(yesterday < today)

    # if(daily_water_usage is None or last_day is None or last_day.strftime("%Y-%m-%d") < now.strftime("%Y-%m-%d")):
    #     daily_water_usage = get_daily_random_water_usage()
    #     last_day = now

    now = datetime.now()
    print(now.hour, now.minute)

    # while True:
    #     now = datetime.now()
    #     m = now.minute
    #     s = now.second

    #     nb_of_step_per_hour = int(3600/config.delay)
    #     test = s % config.delay

    #     if(test == 0):
    #         step = int((m * 60 + s) / config.delay)
    #         print("{} / 120".format(step))

    #     time.sleep(1)

    # print(gce.get_water_info())
    # water_daily_consumption, water_counter_index = gce.get_water_indexes()
    # print("{now} - {water_daily_consumption} - {water_counter_index}".format(now=datetime.now().strftime("%Y-%m-%d %X"),
    #                                                                          water_daily_consumption=water_daily_consumption, water_counter_index=water_counter_index))
