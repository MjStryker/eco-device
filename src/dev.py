from datetime import datetime
from random import randint

#  From 21:00 to 07:00


def simulate_water_usage(time):
    if ((time.hour > 21 and time.hour <= 23) or (time.hour >= 0 and time.hour < 7)):
        return randint(0, 120) == 0

    return randint(0, 60) == 0


def get_last_db_record(client, data_source: str):
    # return client.query('SELECT LAST(*) FROM {data_source}'.format(data_source=data_source.upper()))
    # return client.query('SELECT * FROM {data_source} GROUP BY * ORDER BY DESC LIMIT 1'.format(data_source=data_source.upper()))
    return client.query('SELECT * FROM {data_source} ORDER BY DESC LIMIT 1'.format(data_source=data_source.upper()))


def generate_random_entry(client, data_source: str):
    now = datetime.now()
    latest_record_query_res = get_last_db_record(client, data_source.upper())
    latest_record = next(latest_record_query_res.get_points())

    latest_record_time_str = latest_record["time"]
    latest_record_time_date = datetime.strptime(
        latest_record_time_str, "%Y-%m-%dT%H:%M:%S.%fZ").day

    daily_consumption = latest_record["daily_consumption"] if latest_record_time_date == now.day else 0
    counter_index = latest_record["counter_index"]

    newvalue = randint(1, 6) if simulate_water_usage(now) else 0

    daily_consumption += newvalue
    counter_index += newvalue

    return (daily_consumption, counter_index)


if __name__ == "__main__":
    now = datetime.now()
    print(now.astimezone())
    # water_daily_consumption, water_counter_index = (0, 0)
    # simulate_water_usage(now)
    # res = {"True": 0,
    #        "False": 0}
    # for i in range(50):
    #     res["{}".format(randint(0, 15) == 0)] += 1
    # print(res)
