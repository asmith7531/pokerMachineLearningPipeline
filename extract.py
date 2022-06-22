import os
import tarfile


def extract(tarFile, extract_path='.'):
    tar = tarfile.open(tarFile, 'r')
    for item in tar:
        #print(item)
        tar.extract(item, extract_path)
        if (item.name.find(".tgz") != -1) and (("holdem" not in item.name) or ("nolimit" not in item.name)):
            try:
                extract(item.name, "./" + item.name[:item.name.rfind('/')])
                os.remove(item.name)
            except:
                pass


def removeOtherFiles() -> None:
    dir = "IRCdata"
    for f in os.listdir(dir):
        print(f)
        try:
            """We can just remove all the remaining files in the directory, because OS remove will not impact our newly 
            extracted directories. It only works on files."""
            os.remove(os.path.join(dir, f))
        except:
            pass


extract("IRCdata.tgz")
removeOtherFiles()
