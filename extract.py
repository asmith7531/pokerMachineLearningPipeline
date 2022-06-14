import os
import sys
import tarfile
import shutil
from os import path
from os import walk


def extract(tarFile, extract_path='.'):
    tar = tarfile.open(tarFile, 'r')
    for item in tar:
        print(item)
        tar.extract(item, extract_path)
        if (item.name.find(".tgz") != -1) and ((item.name.find("holdem") != -1) or (item.name.find("nolimit") != -1)):
            try:
                extract(item.name, "./" + item.name[:item.name.rfind('/')])
                os.remove(item.name)
            except:
                pass


dir = "IRCdata"


def removeNoneHoldemTars() -> None:
    directories = []
    for (dirnames) in walk("IRCdata"):
        directories = dirnames
        break
    directories = directories[1]
    for dir in directories:
        if "holdem" not in dir:
            path = dir + "/" + str(dir)
            shutil.rmtree(path)


def removeOtherFiles() -> None:
    for f in os.listdir(dir):
        try:
            os.remove(os.path.join(dir, f))
        except:
            pass


extract("IRCdata.tgz")
removeNoneHoldemDirs()
removeOtherFiles()

