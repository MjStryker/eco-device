from enum import Enum, auto

#          1 : 1 second
#   x     60 : 1 minute
#   x   3600 : 1 hour
#   x     24 : 1 day
#     ------
#   = 86 400

NB_OF_SECONDS_IN_A_DAY = 86400


class Device_type(Enum):
    WATER = auto()


# homedir = path.expanduser('~')
homedir = "/home"
data_dirname = "eco-devices"

delay = 5  # In seconds
nb_of_steps_per_day = int(NB_OF_SECONDS_IN_A_DAY / delay)

filename_date_format = "%Y_%m_%d"
file_extension = ".csv"
file_separator = ";"
