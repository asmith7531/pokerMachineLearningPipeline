import os
import tarfile
import shutil
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


dirs = "IRCdata"


def removeNoneHoldemTars() -> None:
    files = []
    try:
        for (files) in walk("IRCdata"):
            break
        for tars in files:
            if "holdem" or "nolimit" not in files:
                shutil.rmtree(os.path.join(dirs, files))
    except:
        pass


extract("IRCdata.tgz")
removeNoneHoldemTars()

