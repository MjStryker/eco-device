import os.path
import time
import glob
import ntpath

from datetime import datetime
from random import randint

today = datetime.now()
# dateString = today.strftime("%Y-%m-%d %H:%M:%S")

fileExtension = ".csv"
dirname = "data"

# Format
# ------
# heure (HH:MM:SS) ; index jour ; index total

# Exemple
# -------
# 20:19:25 ; 17 ; 204


def getTodaysFilename():
    return str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2) + "_water_gce_index" + fileExtension


def getLatestFilename():
    files = sorted(filter(lambda file: os.path.isfile(os.path.join(dirname, file)),
                          os.listdir(dirname)))
    if(len(files) == 0):
        return None
    latestFilename = files[-1]
    return latestFilename


def getLastLineFromFile(filename):
    fullPath = os.path.join(dirname, filename)
    lastLine = None
    with open(fullPath, "r") as f:
        lines = f.readlines()
        if (len(lines) > 0):
            lastLine = lines[-1]
    return lastLine


def getLastEntry():
    latestFilename = getLatestFilename()
    if(latestFilename is None):
        return None
    return getLastLineFromFile(latestFilename)

# def updateFileValue(filename, data):
#     fullPath = os.path.join(path, filename)
#     with open(fullPath, "w") as f:
#         f.write(data)


def addDataToFile(filename, hour, data):
    fullPath = os.path.join(dirname, filename)
    with open(fullPath, "a") as f:
        newLineData = [hour] + data
        print(newLineData)
        newLineStr = ";".join(newLineData)
        f.write(newLineStr + "\n")


def getIndexTotal():
    lastEntry = getLastEntry()
    total = 0 if lastEntry is None else lastEntry.split(";")[-1].rstrip()
    return int(total)


# def getLastIndexValue():
#     lastEntry = getLastLineFromFile(filename)
#     total = 0 if lastEntry is None else lastEntry.split(";")[-2].rstrip()
#     return total


def generateRandomValues(n):
    todaysFilename = getTodaysFilename()
    for i in range(n):
        total = getIndexTotal()
        newValue = randint(0, 20) if randint(0, 1) == 1 else 0
        if(newValue > 0):
            now = datetime.now()
            hour = str(now.hour).zfill(2) + ":" + \
                str(now.minute).zfill(2) + ":" + str(now.second).zfill(2)
            total += newValue
            data = [str(newValue), str(total)]
            addDataToFile(todaysFilename, hour, data)
        else:
            print("0")
        time.sleep(1)


def addEntry(date, idx_jour, idx_total):
    filename = getTodaysFilename()
    hour = str(date.hour).zfill(2) + ":" + \
        str(date.minute).zfill(2) + ":" + str(date.second).zfill(2)
    data = [str(idx_jour), str(idx_total)]
    addDataToFile(filename, hour, data)


if __name__ == "__main__":
    # print(getIndexTotal())
    generateRandomValues(50)
