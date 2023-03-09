from sys import argv
if len(argv) == 1:
    print("No Files Specified!")

import cv2
import hashcmp
import os
from os import system

print("processing " + str(len(argv) - 1) + " files")
processcnt = 0

for name in argv[1:]:    
    if len(name.split('.')) < 2:
        print("error found with: " + name)
        continue
    suffix = os.path.splitext(name)[-1][1:]
    if suffix != "png":
        continue
    # record the sha-256 digest 
    base64before = hashcmp.hashfile(name)
    # do not change the picture color channels
    raw_pic = cv2.imread(name, -1)
    # print("processing " + name)
    # modify the last pixel slightly
    # note that the picture can be grey scaled
    try:
        if len(raw_pic.shape) == 3:
            lenk = min(raw_pic.shape[0], raw_pic.shape[1])
            for i in range(5, lenk-5):
                if raw_pic[i][i][0] <= 127:
                    raw_pic[i][i][0] += 1
                else:
                    raw_pic[i][i][0] -= 1
            # if raw_pic.shape[2] == 4:
            #     # print(raw_pic.shape)
            #     lenk = min(raw_pic.shape[0], raw_pic.shape[1])
            #     for i in range(lenk):
            #         if raw_pic[i][i][0] <= 127:
            #             raw_pic[i][i][0] += 1
            #         else:
            #             raw_pic[i][i][0] -= 1
            # else:
            #     if raw_pic[raw_pic.shape[0]-2][raw_pic.shape[1]-2][0] <= 127:
            #         raw_pic[raw_pic.shape[0]-2][raw_pic.shape[1]-2][0] += 1
            #     else:
            #         raw_pic[raw_pic.shape[0]-2][raw_pic.shape[1]-2][0] -= 1
        else:
            if raw_pic[raw_pic.shape[0]-1][raw_pic.shape[1]-1] <= 127:
                raw_pic[raw_pic.shape[0]-1][raw_pic.shape[1]-1] += 1
            else:
                raw_pic[raw_pic.shape[0]-1][raw_pic.shape[1]-1] -= 1
            # raw_pic[raw_pic.shape[0]-1][raw_pic.shape[1]-1] += 1
        # overwrite
        cv2.imwrite(name, raw_pic)
        base64after = hashcmp.hashfile(name)
        # print(base64after, base64before)
        if base64before != base64after:
            processcnt += 1
    except (Exception, BaseException) as e:
        print(e)
        continue

print("successfully modified " + str(processcnt))