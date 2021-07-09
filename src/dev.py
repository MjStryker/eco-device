import time
import fileManager

from typing import List
from datetime import datetime
from random import randint


def getIndexTotal():
    lastEntry = fileManager.getLastEntry()
    total = 0 if lastEntry is None else lastEntry.split(";")[-1].rstrip()
    return int(total)


def generateRandomEntry() -> List[int]:
    total = getIndexTotal()
    newValue = randint(0, 20) if randint(0, 2) == 1 else 0
    if(newValue > 0):
        total += newValue
        return [newValue, total]
    return [0, total]


def addRandomIndexesToFile(n: int):
    for i in range(n):
        gce_index_jour, gce_index_total = generateRandomEntry()
        try:
            fileManager.addIndexesToFile(gce_index_jour, gce_index_total)
            time.sleep(1)
        except ValueError as err:
            print(err)


if __name__ == "__main__":
    addRandomIndexesToFile(20)
