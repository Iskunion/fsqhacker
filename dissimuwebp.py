import cv2
import os
from sys import argv
from PIL import Image, ImageOps

def webp2png(webp):
    prefix = os.path.splitext(webp)[0]
    image = Image.open(webp)
    image = ImageOps.exif_transpose(image)
    png = prefix + ".png"
    image.save(png)
    return png
    
def png2webp(png):
    prefix = os.path.splitext(png)[0]
    image = Image.open(png)
    webp = prefix + ".webp"
    image.save(webp, "WEBP")

if __name__ == "__main__":
    if len(argv) == 1:
        print("No Files Specified!")
    print("processing " + str(len(argv) - 1) + " files")

    for name in argv[1:]:
        
        if len(name.split('.')) < 2:
            print("error found with: " + name)
            continue
        suffix = os.path.splitext(name)[-1][1:]
        if suffix != "webp":
            continue
        png_name = webp2png(name)
        # do not change the picture color channels
        raw_pic = cv2.imread(png_name, -1)
        # print("processing " + name)
        # modify the last pixel slightly
        # note that the picture can be grey scaled
        try:
            if len(raw_pic.shape) == 3:
                if raw_pic[raw_pic.shape[0]-1][raw_pic.shape[1]-1][0] <= 127:
                    raw_pic[raw_pic.shape[0]-1][raw_pic.shape[1]-1][0] += 1
                else:
                    raw_pic[raw_pic.shape[0]-1][raw_pic.shape[1]-1][0] -= 1
            else:
                if raw_pic[raw_pic.shape[0]-1][raw_pic.shape[1]-1] <= 127:
                    raw_pic[raw_pic.shape[0]-1][raw_pic.shape[1]-1] += 1
                else:
                    raw_pic[raw_pic.shape[0]-1][raw_pic.shape[1]-1] -= 1
            # overwrite
            cv2.imwrite(png_name, raw_pic)
            png2webp(png_name)
            os.remove(png_name)
        except:
            continue