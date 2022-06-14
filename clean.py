import os
import shutil
import csv
from CleanHands import CleanHands


def parsePokerTables(folder: str) -> None:
    gamePath = os.path.join("IRCdata", folder)
    dirsToParse = os.listdir(gamePath)
    for dirs in dirsToParse:
        try:
            parseHands(os.path.join(gamePath, dirs))
            parseRoster()
        except:
            """removing the poker table if there is a hdb file missing"""
            #shutil.rmtree(os.path.join(gamePath, dirs))


def parseHands(tablePath) -> None:
    tablePath = os.path.join(tablePath, "hdb")
    with open(tablePath) as hdbFile:
        for line in hdbFile:
            splitLine = line.split(" ")
            cleanHands.hand_id.append(splitLine[0])


def parseRoster(tablePath) -> None:
    tablePath = os.path.join(tablePath, "hroster")
    print(tablePath)
    # open the output csv file in the write mode

    with open(tablePath) as rosterFile:
        for line in rosterFile:
            splitLine = line.split(" ")
            #cleanHands.hand_id.append(splitLine[0])

cleanHands = CleanHands()
parsePokerTables("holdem1")
print(cleanHands.hand_id)

with open('cleanHands.csv') as cleanHands:
    csvWriter = csv.writer(cleanHands, delimiter=',')
    csvWriter
