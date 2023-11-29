from sys import argv
from os import system

import hashcmp
import os

import xml.etree.ElementTree as ET
if __name__ == "__main__":
    if len(argv) == 1:
        print("No Files Specified!")
    print("processing " + str(len(argv) - 1) + " files")
    processcnt = 0
    for name in argv[1:]:
        if len(name.split('.')) < 2:
            print("error found with: " + name)
            continue
        suffix = os.path.splitext(name)[-1][1:]
        if suffix != "xml":
            continue
        base64before = hashcmp.hashfile(name)
        tree = ET.parse(name)
        root = tree.getroot()
        root.set("hacker", "cz")
        tree.write(name)
        base64after = hashcmp.hashfile(name)
        # print(base64after, base64before)
        if base64before != base64after:
            processcnt += 1

    print("successfully modified " + str(processcnt))
