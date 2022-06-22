import os
import csv


def parsePokerTables(folder: str) -> None:
    gamePath = os.path.join("IRCdata", folder)
    dirsToParse = os.listdir(gamePath)
    for dirs in dirsToParse:
        try:
            parseHDB(os.path.join(gamePath, dirs))
        except (Exception, SyntaxError, KeyError, ValueError) as e:
            print(e)


def parseHDB(tablePath) -> None:
    """This opens each Hands Database File and parses it for hand IDs, betting rounds with the number of players/pot
    sizes, and the board cards, calls the functions to parse related files, then writes the object to json and calls
    the function to open the json file and append the object """
    tablePathHDB = os.path.join(tablePath, "hdb")

    with open(tablePathHDB, 'r') as hdbFile:
        hdbString = hdbFile.readlines()
        hdbFile.close()
    for line in hdbString:
        splitLine = line.split()
        try:
            """instantiating the hand class"""
            csvString = ''
            """assigning the hand id"""
            csvString += str(splitLine[0])
            """assigning the number of players in the hand"""
            csvString += " " + str(splitLine[3])
            """assigning the betting rounds"""
            for bet in range(0, 4):
                try:
                    split = splitLine[bet + 4].split("/")
                    playersLeft = split[0]
                    potSize = split[1]
                    csvString += " " + playersLeft + " " + potSize
                except (Exception, SyntaxError, KeyError, ValueError) as e:
                    csvString += " " + "NA"
                    print(e)
            """assigning the board cards to the instance"""
            for card in range(0, 5):
                try:
                    csvString += " " + splitLine[card + 8]
                except (Exception, SyntaxError, KeyError, ValueError) as e:
                    csvString += " " + "NA"
                    print(e)
            """calling the parseRoster function to get players in the hand"""
            parseRoster(tablePath, csvString)
        except (Exception, SyntaxError, KeyError, ValueError) as e:
            print(e)


def parseRoster(tablePath: str, csvString: str) -> None:
    """This parses the hroster files, matches the hand id and adds the player names to the csvString """
    try:
        tablePathRoster = os.path.join(tablePath, "hroster")
        with open(tablePathRoster, 'r') as rosterFile:
            rosterString = rosterFile.readlines()
            rosterFile.close()
        for line in rosterString:
            splitLine = line.split(" ")
            _id = csvString.split()
            if int(splitLine[0]) == int(_id[0]):
                for player in splitLine[4:]:
                    """the last player in this file always has a "\n" appended. We need to remove it to match to the 
                    player file """
                    cleanedPlayer = player.replace("\n", "")
                    """calling the assignPlayerData function to get player specific data"""
                    assignPlayerData(tablePath, cleanedPlayer, csvString)
    except (Exception, SyntaxError, KeyError, ValueError) as e:
        print(e)


def assignPlayerData(tablePath, player, csvString):
    csvString += " " + player
    "for each player"
    parsePDB(tablePath, csvString, player)


def parsePDB(tablePath, csvString, player) -> None:
    """"This function opens the player file containing player specific data on all hands they played, finds the
    matching hand ID and adds pocket cards, player action and position, bankrol and winnings if they won the hand """
    tablePathPDB = os.path.join(tablePath, "pdb", ("pdb." + str(player)))
    try:
        with open(tablePathPDB) as playerData:
            playerString = playerData.readlines()
            playerData.close()
        for line in playerString:
            playerData = csvString
            """splitting to get the hand id"""
            playerArray = line.split()
            stringSplit = csvString.split()
            """if the hand id in the player line and our hand string match, assign player data"""
            if int(playerArray[1]) == int(stringSplit[0]):
                """bankroll"""
                # cleanHands.players[player]["bankroll"] = playerList[8]
                playerData += " " + playerArray[8]
                #print(playerList)
                """action (ie how much money put into the hand by player)"""
                # playerData += playerList[9]
                """seat position"""
                playerData += " " + playerArray[3]
                """playerActions at each game stage"""
                # playerData += [playerList[4:8]]
                """pocketCards held in the players hand"""
                # playerData += playerList[11:]
                """winnings - this corresponds to an integer value with the amount they won, I don't care how much 
                they won, just whether they won or lost the hand"""
                if int(playerArray[10]) > 0:
                    playerData += " " + str(1)
                else:
                    playerData += " " + str(0)
                """checking that the csvFile is the proper length before appending to the csvFile"""
                if len(playerData.split()) == 19:
                    print(playerData)
                    dataToCSV(playerData)
                else:
                    """if it is not the proper length, just pass and do not append"""
                    pass
    except (Exception, SyntaxError, KeyError, ValueError) as e:
        print(e)


def dataToCSV(cleanHand):
    dataFile = open('handCSV.csv', 'a')
    csv_writer = csv.writer(dataFile)
    csv_writer.writerow(cleanHand.split())


def initializeCSV(fileName: str) -> None:
    """writing the """
    dataFile = open(fileName, "a")
    csvWriter = csv.writer(dataFile)
    csvWriter.writerow(["Hand ID", "PlayersInGame", "NumPlayersPreFlop", "PotPreFlop", "NumPlayersPostFlop", "PotPostFlop", "NumPlayersTurn", "PotTurn", "NumPlayersShowdown", "PotShowdown", "Flop1", "Flop2", "Flop3", "Turn", "River", "UserName", "Bankroll", "Position", "Win"])


initializeCSV("handCSV.csv")
parsePokerTables("holdem")
