import os
import config

from datetime import datetime
from pathlib import Path


# Format
# ------
# hour (HH:MM:SS) ; index day ; index total

# Example
# -------
# 20:19:25 ; 17 ; 204


def get_data_dir_path(data_source: config. data_source):
     data_source = data_source.name.lower()
    return os.path.join(config.homedir, config.data_dirname,  data_source)


def get_file_dir_path(date: datetime,  data_source: config. data_source):
    dirPath = get_data_dir_path( data_source)
    year, month = date.strftime("%Y"), date.strftime("%m")
    return os.path.join(dirPath, year, month)


def get_filename(date: datetime,  data_source: config. data_source):
     data_source =  data_source.name.lower()
    dateFormatted = date.strftime(
        config.filename_date_format)
    filenameElts = [dateFormatted, "gce_device",  data_source, "index"]
    return "_".join(filenameElts) + config.file_extension


def get_file_fullpath(date: datetime,  data_source: config. data_source):
     data_source =  data_source.name.lower()
    return os.path.join(get_file_dir_path(date, config. data_source.WATER), get_filename(date, config. data_source.WATER))


def create_dir_if_does_not_exist(dirpath: str):
    if(not os.path.isdir(dirpath)):
        print("Directory '" + dirpath + "' does not exist and will be created")
    Path(dirpath).mkdir(parents=True, exist_ok=True)


def create_file_if_does_not_exist(filepath: str):
    if(not os.path.isfile(filepath)):
        print("File '" + filepath + "' does not exist and will be created")
    file = Path(filepath)
    file.touch(exist_ok=True)


def append_data_to_file(dirpath: str, filename: str, data: str):
    filepath = os.path.join(dirpath, filename)
    create_dir_if_does_not_exist(dirpath)
    create_file_if_does_not_exist(filepath)
    with open(filepath, "a") as f:
        f.write(data + "\n")


def get_file_nb_lines(date: datetime):
    filepath = get_file_fullpath(date, config. data_source.WATER)
    create_file_if_does_not_exist(filepath)
    with open(filepath, "r") as f:
        return len(f.readlines())


def add_indexes(date: datetime, water_daily_consumption: int, water_counter_index: int):
    dirpath = get_file_dir_path(date, config. data_source.WATER)
    filename = get_filename(date, config. data_source.WATER)
    hour = date.strftime("%X")

    data = [hour, water_daily_consumption, water_counter_index]
    dataStr = config.file_separator.join([str(e) for e in data])

    append_data_to_file(dirpath, filename, dataStr)


if __name__ == "__main__":
    try:
        print()
        # now = datetime.now()
        # add_indexes(now, 5, 23)
    except ValueError as err:
        print(err)
