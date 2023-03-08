from sys import argv
from os import system
import xml.etree.ElementTree as ET
if __name__ == "__main__":
    if len(argv) == 1:
        print("No Files Specified!")
    print("processing " + str(len(argv) - 1) + " files")

    for name in argv[1:]:
    
        if len(name.split('.')) < 2:
            print("error found with: " + name)
            continue
        suffix = name.split('.')[-1]
        if suffix != "xml":
            continue
        tree = ET.parse(name)
        root = tree.getroot()
        root.set("hacker", "cz")
        tree.write(name)


