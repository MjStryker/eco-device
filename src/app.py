
import config
import gce.devices.water as gce

from datetime import datetime
from influxdb import InfluxDBClient
from dotenv import load_dotenv

import os
import sys
import time


# import file_manager
from dev import generate_random_entry

load_dotenv()

ENV = os.getenv("ENV") or "dev"

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER_NAME = os.getenv("DB_USER_NAME")
DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD")


# TODO: Add backup config (something like this)
# -----------------------
# influx backup /path/to/backup/dir/backup_name_$(date '+%Y-%m-%d_%H-%M')

# Open InfluxDB CLI
# -----------------
# influx -precision rfc3339 -database eco_device_db

# Change default retention policy to 5 years
# ------------------------------------------
# ALTER RETENTION POLICY "autogen" ON "eco_device_db" DURATION 1825d
# SHOW RETENTION POLICIES

# Basic SQL select operation
# --------------------------
# SELECT daily_consumption FROM WATER ORDER BY DESC LIMIT 1


def wait_for_db_to_be_ready():
    time.sleep(5)


def get_db_client():
    return InfluxDBClient(host=DB_HOST, port=DB_PORT,
                          username=DB_USER_NAME, password=DB_USER_PASSWORD, database=DB_NAME)


water_data_source = config.data_source.WATER.name.upper()


def job(client):
    now = datetime.now()

    if(ENV == "prod"):
        water_daily_consumption_in_liter, water_counter_index_in_liter = gce.get_water_indexes()

    elif(ENV == "dev"):
        water_daily_consumption_in_liter, water_counter_index_in_liter = generate_random_entry(
            client, water_data_source)

    # water_daily_consumption_in_liter, water_counter_index_in_liter = (0, 0)

    json_body = [{
        "measurement": water_data_source,
        "tags": {},
        "time": now.astimezone(),
        "fields": {
            "daily_consumption": water_daily_consumption_in_liter,
            "counter_index": water_counter_index_in_liter
        }}]

    print("{now} - {water_daily_consumption_in_liter} - {water_counter_index_in_liter}".format(now=now.strftime("%Y-%m-%d %X"),
                                                                                               water_daily_consumption_in_liter=water_daily_consumption_in_liter, water_counter_index_in_liter=water_counter_index_in_liter))

    client.write_points(json_body)


def wait_until_time_delay():
    while True:
        now = datetime.now()
        if(now.second % config.delay == 0):
            break
        time.sleep(.2)


def loop(client):
    start_time = time.time()
    while True:
        wait_until_time_delay()
        job(client)
        time.sleep(config.delay - ((time.time() - start_time) % config.delay))


if __name__ == "__main__":
    try:
        wait_for_db_to_be_ready()
        client = get_db_client()
        loop(client)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

# def job():
#     now = datetime.now()
#     job_nb = file_manager.get_file_nb_lines(now) + 1

#     if(ENV == "prod"):
#         water_daily_consumption_in_liter , water_counter_index_in_liter  = gce.get_water_indexes()
#         print(" Index jour :", water_daily_consumption_in_liter ,
#               "\nIndex total :", water_counter_index_in_liter )

#     elif(ENV == "dev"):
#         water_daily_consumption_in_liter , water_counter_index_in_liter  = dev.generate_random_entry(
#             config.data_source.WATER)

#     addedvalue = " (+{})".format(water_daily_consumption_in_liter ) if water_daily_consumption_in_liter  > 0 else ""
#     step_str_format = "[ {} / {} ] ".format(job_nb, config.nb_of_steps_per_day)

#     print(" Index jour :", water_daily_consumption_in_liter,
#           "\nIndex total :", water_counter_index_in_liter)

#     print(step_str_format + datetime.now().strftime("%Y-%m-%d %X") +
#           " -> " + str(water_counter_index_in_liter ) + addedvalue)

#     # if(water_daily_consumption_in_liter  > 0):
#     file_manager.add_indexes(
#         datetime.now(), water_daily_consumption_in_liter , water_counter_index_in_liter )
