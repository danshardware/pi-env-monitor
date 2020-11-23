#!/usr/bin/python3
import os
import sys
import getopt
import glob
import json
from datetime import datetime
from datetime import timedelta
from pathlib import Path

# this is a hack from https://stackoverflow.com/questions/1447287/format-floats-with-standard-json-module 
# to keep the floats encoded to only 2 digits of precision
from json import encoder
encoder.FLOAT_REPR = lambda o: "%.2f" % o

''' This program grabs the latest n sample files from the given folder and creates 
    Time series data JSON output for temperature, humidity, and pressure '''

def usage():
    print('''
    Usage: calculateTimeSeries [ -d|--dir data_directory ] [ -o|--out outputFile.json ]
        [ -a|--age max_age_in_seconds ] 
    ''')

# Pull parameters from command line, ENV, and finally, defaults

dataDir = os.getenv('DATA_DIR') or '/var/pi-env/captures'
numOfEvents = os.getenv('NUM_EVENTS') or (12 * 24) # a day's worth
outFile = os.getenv('OUT_FILE') or '-'
fileGlob = os.getenv('FILE_GLOB') or '20[0-9][0-9]*.json'
maxAge = os.getenv('MAX_AGE') or (3600 * 24)
maxAge = int(maxAge)
includeImage = os.getenv('IMAGE') or ""

# Checks if a file has a sample date earlier than specified
def dataYoungerThan(when, where):
    try:
        with open(where) as f:
            data = json.load(f)
            f.close()
    except Exception as e:
        print('Error opening {}: '.format(where), e)
        return False
    
    sampleDateTime = datetime.strptime(data["timestamp"], '%Y-%m-%d %H:%M:%S')
    if sampleDateTime < when:
        # add a python-approved datetime object to the return value to make further operations easier
        data["datetime"] = sampleDateTime
        return data
    else:
        return False

# scan the folder for files in our search criteria, and compiles an array of matching entries
def scanFolder():
    outputData = []
    try:
        dataDirOperator = Path(dataDir)
        if not dataDirOperator.exists():
            print ("unable to open {}".format(dataDirOperator.name), file=sys.stderr)
            return False
        files = dataDirOperator.glob(fileGlob)
        earliest = datetime.now() - timedelta(seconds=(-1 * maxAge))
    except Exception as e:
        print ("Error scanning data directory: ", e, file=sys.stderr)
        return False

    for f in files:
        try:
            fileInfo = dataYoungerThan(earliest, f)
            if fileInfo != False:
                outputData.append(fileInfo)
        except Exception as e:
            print ("Error scanning data directory: ", e, file=sys.stderr)

    return outputData

def getTimestamp(item):
    return item["datetime"]

def compileTSD(data):
    outputData = []
    # sort the input data by timestamps
    data.sort(key=getTimestamp)

    # format for each row is timestamp, temp_last/ave/max/min, humidity_last/ave/max/min, pressure_last/ave/max/min
    for row in data:
        outputData.append([
            row["timestamp"], 
            row["temperature"]["last"], row["temperature"]["avg"], row["temperature"]["max"], row["temperature"]["min"], 
            row["humidity"]["last"], row["humidity"]["avg"], row["humidity"]["max"], row["humidity"]["min"], 
            row["pressure"]["last"], row["pressure"]["avg"], row["pressure"]["max"], row["pressure"]["min"]
        ])
    return outputData

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hd:o:n:a:i:",["dir=","out=", "num=", "age=", "img="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-d", "--dir"):
            dataDir = arg
        elif opt in ("-o", "--out"):
            outFile = arg
        #elif opt in ("-n", "--num"):
        #    numOfEvents = arg
        elif opt in ("-a", "--age"):
            maxAge = int(arg)
        elif opt in ("-i", "--img"):
            includeImage = arg

    # Parse all the data files into time series data
    data = scanFolder()
    if data == False:
        sys.exit(1)
    
    # Compile the TSD
    tsd = compileTSD(data)

    # Add metadata
    outputData = {
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "image": includeImage,
        "data": tsd
    }

    # spit it out
    if outFile == "-":
        print(json.dumps(outputData))
    else:
        try:

            with open(Path(outFile)) as f:
                json.dump(outputData, f)
                f.close()
        except Exception as e:
            print('Error opening {}: '.format(outFile), e)
            sys.exit(2)
