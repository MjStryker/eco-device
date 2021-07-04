import os.path
import time

from datetime import datetime
from random import randint

today = datetime.now()
dateString = today.strftime("%Y-%m-%d %H:%M:%S")

fileExtension = ".xlsx"

# Format
# ------
# heure (HH:MM:SS) ; index jour ; index total

# Exemple
# -------
# 20:19:25 ; 17 ; 204


def getFilename():
    return str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2) + "_water_gce_index" + fileExtension


def getLastLineFromFile(filename, path="data"):
    fullPath = os.path.join(path, filename)
    lastLine = None
    with open(fullPath) as f:
        lines = f.readlines()
        if (len(lines)):
            lastLine = lines[-1]
    return lastLine


def updateFileValue(filename, data, path="data"):
    fullPath = os.path.join(path, filename)
    with open(fullPath, "w") as f:
        f.write(data)


def addDataToFile(filename, hour, data, path="data"):
    fullPath = os.path.join(path, filename)
    with open(fullPath, "a") as f:
        newLineData = [hour] + data
        print(newLineData)
        newLineStr = ";".join(newLineData)
        f.write(newLineStr + "\n")


def test():
    filename = getFilename()
    lastEntry = getLastLineFromFile(filename)
    total = 0 if lastEntry is None else lastEntry.split(";")[-1].rstrip()
    print("Total:", total)


def generateRandomValues(n):
    filename = getFilename()
    for i in range(n):
        lastEntry = getLastLineFromFile(filename)
        total = 0 if lastEntry is None else int(
            lastEntry.split(";")[-1].rstrip())
        newValue = randint(0, 20) if randint(0, 1) == 1 else 0
        if(newValue > 0):
            now = datetime.now()
            hour = str(now.hour).zfill(2) + ":" + \
                str(now.minute).zfill(2) + ":" + str(now.second).zfill(2)
            total += newValue
            data = [str(newValue), str(total)]
            addDataToFile(filename, hour, data)
        else:
            print("0")
        time.sleep(5)


if __name__ == "__main__":
    # addDataToFile()
    generateRandomValues(50)
