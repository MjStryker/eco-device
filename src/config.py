from os import path
from enum import Enum, auto


class Device_type(Enum):
    WATER = auto()


homedir = path.expanduser('~')
data_dirname = "eco-devices"

filename_date_format = "%Y-%m-%d"
file_extension = ".csv"
file_separator = ";"
