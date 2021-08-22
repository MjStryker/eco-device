from datetime import datetime, timezone
from random import randint, shuffle

import config

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


# def simulate_water_usage(time):
#     if ((time.hour > 21 and time.hour <= 23) or (time.hour >= 0 and time.hour < 7)):
#         return randint(0, 120) == 0

#     return randint(0, 25) == 0


def get_last_db_record(client, data_source: str):
    # return client.query('SELECT LAST(*) FROM {data_source}'.format(data_source=data_source.upper()))
    # return client.query('SELECT * FROM {data_source} GROUP BY * ORDER BY DESC LIMIT 1'.format(data_source=data_source.upper()))
    return client.query('SELECT * FROM {data_source} ORDER BY DESC LIMIT 1'.format(data_source=data_source.upper()))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


daily_random_water_usage = None


def generate_random_entry(client, data_source: str, time: datetime):
    global daily_random_water_usage

    if(daily_random_water_usage is None or (time.hour == 0 and time.minute == 0)):
        print("Generating new daily water usage...")
        daily_random_water_usage = get_daily_random_water_usage()

    latest_record_query_res = get_last_db_record(client, data_source.upper())

    latest_record_list = list(latest_record_query_res.get_points())

    if(len(latest_record_list) == 0):
        return (0, 0)

    latest_record = latest_record_list[0]
    # latest_record = next(latest_record_query_res.get_points())

    latest_record_time_str = latest_record["time"]
    latest_record_time_date = utc_to_local(datetime.strptime(
        latest_record_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")).day

    daily_consumption = latest_record["daily_consumption"] if latest_record_time_date == time.day else 0
    counter_index = latest_record["counter_index"]

    # new_value = randint(1, 10) if simulate_water_usage(time) else 0
    step = int((time.minute * 60 + time.second) / config.delay)
    new_value = daily_random_water_usage[time.hour][step]

    daily_consumption += new_value
    counter_index += new_value

    return (daily_consumption, counter_index)


if __name__ == "__main__":
    # now = datetime.now()
    # print(now.astimezone())
    fake_last_record_time_str = "2021-08-16T22:56:30.001017Z"
    fake_last_record_time_date = datetime.strptime(
        fake_last_record_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    print(utc_to_local(fake_last_record_time_date))
