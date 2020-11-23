#!/usr/bin/python3

import os
import sys
import getopt
import glob
import json
from pathlib import Path
from PIL import Image

version = "2020-11-23.00"

def resizeWithAspect(srcFile, destFile, maxX, maxY, q):
    # Deal with the source file
    try:
        im = Image.open(srcFile)
        xSize, ySize = im.size
        srcAspectRatio = float(xSize)/ySize
        dstAspectRaio = float(maxX)/maxY
        scaleFactor = float(maxX)/xSize
        if srcAspectRatio > dstAspectRaio:
            # input is wider than max output size. Set ratio based on X sizes, which is the default
            pass
        else:
            # input is taller than ouput. scale based on Y
            scaleFactor = maxY/ySize
    except Exception as e:
        print ("Error opening or reading {}: ".format(srcFile), e, file=sys.stderr)
        return False
    
    # do the resize and write it to the destination file
    try:
        new_image_size = (int(xSize * scaleFactor), int(ySize * scaleFactor))
        im = im.resize(new_image_size, Image.BICUBIC)
        new_im = Image.new("RGB", new_image_size)
        new_im.paste(im,(0,0))
        new_im.save(destFile, 'JPEG', quality=q)
    except Exception as e:
        print ("Error writing {}: ".format(destFile), e, file=sys.stderr)
        return False

def usage():
    print('''
    Usage: makeThumbnail.py [options] file[ file... ]
        Options:
            -d|--destination    Destination folder. Defaults to same directory. Relative to the image's direcotry, not the cwd.
                                    If you need that , supply an absolute path
            -s|--suffix         added to filename. Defaults to '_thumb'
            -x                  Maximum X size. Defaults to 320.
            -y                  Maximum Y size. Defaults to 240.
            -q|--quality        JPEG quality. Defaults to 85.
            -h|--help           This message
            -v|--version        Prints the version and exits
    ''')

def printVersion():
    print (version)

if __name__ == "__main__":
    optDest = './'
    optSuffix = '_thumb'
    optQuality = 85
    optX = 320
    optY = 240

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hvd:s:x:y:q:",["destination=","suffix=", "quality=", "help", "version"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--version"):
            printVersion()
            sys.exit()
        elif opt in ("-d", "--destination"):
            optDest = arg
        elif opt in ("-s", "--suffix"):
            optSuffix = arg
        elif opt in ("-q", "--quality"):
            optQuality = arg
        elif opt == '-x':
            optX = arg
        elif opt == '-y':
            optY = arg
        
    for f in args:
        # convert the file to a Path object
        sourceFilePath = Path(f)

        # add the destination if it's relative, or replace if absolute (default behavior in Path lib)
        destFilePath = sourceFilePath.parent / optDest / (sourceFilePath.stem + optSuffix + '.jpg')

        # resize
        resizeWithAspect(f, str(destFilePath), optX, optY, optQuality)

