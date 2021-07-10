from genericpath import isfile
import os
import config

from datetime import datetime
from pathlib import Path


# Format
# ------
# heure (HH:MM:SS) ; index jour ; index total

# Exemple
# -------
# 20:19:25 ; 17 ; 204


# def is_device_type_instance(device_type: config.Device_type):
#     if(not isinstance(device_type, config.Device_type)):
#         raise ValueError("Error: device_type '" + device_type +
#                          "' must be an instance of Enum 'Device_type'")
#     return True


def get_data_dir_path(device_type: config.Device_type):
    # is_device_type_instance(device_type)
    device_type = device_type.name.lower()
    return os.path.join(config.homedir, config.data_dirname, device_type)


def get_file_dir_path(date: datetime, device_type: config.Device_type):
    dirPath = get_data_dir_path(device_type)
    year, month = date.strftime("%Y"), date.strftime("%m")
    return os.path.join(dirPath, year, month)


def get_filename(date: datetime, device_type: config.Device_type):
    # is_device_type_instance(device_type)
    device_type = device_type.name.lower()
    dateFormatted = date.strftime(
        config.filename_date_format)
    filenameElts = [dateFormatted, "gce_device", device_type, "index"]
    return "_".join(filenameElts) + config.file_extension


def get_file_fullpath(date: datetime, device_type: config.Device_type):
    # is_device_type_instance(device_type)
    device_type = device_type.name.lower()
    return os.path.join(get_file_dir_path(date, config.Device_type.WATER), get_filename(date, config.Device_type.WATER))


def create_dir_if_does_not_exist(dirpath):
    if(not os.path.isdir(dirpath)):
        print("Directory '" + dirpath + "' does not exist and will be created")
    Path(dirpath).mkdir(parents=True, exist_ok=True)


def create_file_if_does_not_exist(filepath):
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


def add_indexes(date: datetime, gce_index_jour: int, gce_index_total: int):
    # path = get_file_fullpath(date, config.Device_type.WATER)
    dirpath = get_file_dir_path(date, config.Device_type.WATER)
    filename = get_filename(date, config.Device_type.WATER)
    hour = date.strftime("%X")

    data = [hour, gce_index_jour, gce_index_total]
    dataStr = config.file_separator.join([str(e) for e in data])

    # print(dataStr)
    append_data_to_file(dirpath, filename, dataStr)


if __name__ == "__main__":
    try:
        print()
        # now = datetime.now()
        # add_indexes(now, 5, 23)
    except ValueError as err:
        print(err)
