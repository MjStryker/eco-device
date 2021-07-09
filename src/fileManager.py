import os.path
import re

from pathlib import Path
from datetime import datetime
from typing import List

today = datetime.now()
dateString = today.strftime("%Y-%m-%d %H:%M:%S")

fileNameSuffix = "_gce_device_water_index"
fileExtension = ".csv"

dataRootDirectoryName = "data"

# Format
# ------
# heure (HH:MM:SS) ; index jour ; index total

# Exemple
# -------
# 20:19:25 ; 17 ; 204


def getFolderPath():
    return os.path.join(dataRootDirectoryName, str(today.year), str(today.month).zfill(2))


def getTodaysFileName():
    return str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2) + fileNameSuffix + fileExtension


def getTodaysFileFullPath():
    folderPath = getFolderPath()
    fullPath = os.path.join(folderPath, getTodaysFileName())
    Path(folderPath).mkdir(parents=True, exist_ok=True)
    return fullPath


def getLatestFileName():
    folderPath = getFolderPath()
    files = sorted(filter(lambda file: os.path.isfile(os.path.join(folderPath, file)),
                          os.listdir(folderPath)))
    if(len(files) == 0):
        return None
    latestFileName: str = files[-1]
    return latestFileName


def getLastLineFromFile(filePath):
    lastLine = None
    try:
        with open(filePath, "r") as f:
            lines = f.readlines()
            if (len(lines) > 0):
                lastLine = lines[-1]
    except:
        print("File " + filePath + " does not exist and will be created...")
    return lastLine


def addDataToFile(filePath: str, hour: str, data: List[int]):
    if(re.match("^\d{2}:\d{2}:\d{2}$", hour) is None):
        raise ValueError(
            "[addDataToFile] Error: Invalid hour format, expected 'hh:mm:ss', got " + hour)

    with open(filePath, "a") as f:
        newLineData: List[str, int, int] = [hour] + [str(e) for e in data]
        print(dateString, newLineData)
        newLineStr = ";".join(newLineData)
        f.write(newLineStr + "\n")


def getLastEntry():
    filePath = getTodaysFileFullPath()
    if(filePath is None):
        return None
    return getLastLineFromFile(filePath)


def addEntry(date, idx_jour, idx_total):
    fileName = getTodaysFileName()
    hour = str(date.hour).zfill(2) + ":" + \
        str(date.minute).zfill(2) + ":" + str(date.second).zfill(2)
    data = [str(idx_jour), str(idx_total)]
    addDataToFile(fileName, hour, data)


def addIndexesToFile(gce_index_jour: int, gce_index_total: int):
    indexFileFullPath = getTodaysFileFullPath()

    now = datetime.now()
    hour = str(now.hour).zfill(2) + ":" + \
        str(now.minute).zfill(2) + ":" + str(now.second).zfill(2)

    data = [gce_index_jour, gce_index_total]

    addDataToFile(indexFileFullPath, hour, data)


if __name__ == "__main__":
    print(getLastEntry())
    # print(getIndexTotal())
