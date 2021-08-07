from enum import Enum, auto


class Device_type(Enum):
    WATER = auto()


# homedir = path.expanduser('~')
homedir = "/home"
data_dirname = "eco-devices"

delay = 30

filename_date_format = "%Y_%m_%d"
file_extension = ".csv"
file_separator = ";"
