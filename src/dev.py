from datetime import datetime, timezone
from random import randint

#  From 21:00 to 07:00


def simulate_water_usage(time):
    if ((time.hour > 21 and time.hour <= 23) or (time.hour >= 0 and time.hour < 7)):
        return randint(0, 120) == 0

    return randint(0, 25) == 0


def get_last_db_record(client, data_source: str):
    # return client.query('SELECT LAST(*) FROM {data_source}'.format(data_source=data_source.upper()))
    # return client.query('SELECT * FROM {data_source} GROUP BY * ORDER BY DESC LIMIT 1'.format(data_source=data_source.upper()))
    return client.query('SELECT * FROM {data_source} ORDER BY DESC LIMIT 1'.format(data_source=data_source.upper()))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def generate_random_entry(client, data_source: str):
    now = datetime.now()
    latest_record_query_res = get_last_db_record(client, data_source.upper())
    latest_record = next(latest_record_query_res.get_points())

    latest_record_time_str = latest_record["time"]
    latest_record_time_date = utc_to_local(datetime.strptime(
        latest_record_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")).day

    daily_consumption = latest_record["daily_consumption"] if latest_record_time_date == now.day else 0
    counter_index = latest_record["counter_index"]

    newvalue = randint(1, 10) if simulate_water_usage(now) else 0

    daily_consumption += newvalue
    counter_index += newvalue

    return (daily_consumption, counter_index)


if __name__ == "__main__":
    # now = datetime.now()
    # print(now.astimezone())
    fake_last_record_time_str = "2021-08-16T22:56:30.001017Z"
    fake_last_record_time_date = datetime.strptime(
        fake_last_record_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    print(utc_to_local(fake_last_record_time_date))
