import os
import time
import config
import file_manager

from pathlib import Path
from datetime import datetime
from glob import glob
from typing import List
from random import randint


def get_lastline_from_file(filepath):
    lastLine = None
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            if (len(lines) > 0):
                lastLine = lines[-1]
    except:
        print("File " + filepath + " does not exist and will be created...")
    return lastLine


def get_lastdir_from_path(path: str):
    file_manager.create_dir_if_does_not_exist(path)

    dirs = sorted(filter(
        lambda elt:
            os.path.isdir(os.path.join(path, elt))
            and os.listdir(os.path.join(path, elt)),
        os.listdir(path)
    ))

    if (len(dirs) == 0):
        return None

    return dirs[-1]


def get_lastestdir_path(data_source: config. data_source):
    path = file_manager.get_data_dir_path(data_source)

    if(path is None):
        return None

    year = get_lastdir_from_path(path)

    if(year is None):
        return None

    month = get_lastdir_from_path(os.path.join(path, year))

    if(month is None):
        return None

    lastdirpath = os.path.join(path, year, month)

    return lastdirpath


def get_lastfile_path(data_source: config. data_source):
    lastdirpath = get_lastestdir_path(data_source)

    if(lastdirpath is None):
        return None

    files = sorted(filter(lambda file: os.path.isfile(os.path.join(lastdirpath, file)),
                          os.listdir(lastdirpath)))
    if(len(files) == 0):
        return None

    latest_filename: str = files[-1]

    return os.path.join(lastdirpath, latest_filename)


def get_last_entry(data_source: config. data_source):
    filepath = get_lastfile_path(data_source)
    if(filepath is None):
        return None
    return get_lastline_from_file(filepath)


def get_index_total(data_source: config. data_source):
    lastEntry = get_last_entry(data_source)
    total = 0 if lastEntry is None else int(
        lastEntry.split(config.file_separator)[-1].rstrip())
    return total


def generate_random_entry(data_source: config. data_source, step=0, end=0):
    total = get_index_total(data_source)
    newvalue = randint(0, 20) if randint(0, 2) == 1 else 0
    total += newvalue

    return [newvalue, total]


def add_random_indexes(data_source: config. data_source, n: int):
    for i in range(n):
        try:
            daily_consumption, total_index = generate_random_entry(
                data_source, i, n)
            if(daily_consumption > 0):
                file_manager.add_indexes(
                    datetime.now(), daily_consumption, total_index)
            if(i != n):
                time.sleep(1)
        except ValueError as err:
            print(err)


if __name__ == "__main__":
    # print(get_lastestdir_path(config. data_source.WATER))
    # print(get_lastfile_path(config. data_source.WATER))
    # print(get_lastestdir_path(config. data_source.WATER))
    # print(get_last_entry(config. data_source.WATER))
    add_random_indexes(config. data_source.WATER, 2)
