#!/usr/bin/python
import os, sys, subprocess, shlex, re, fnmatch, collections
from subprocess import call
from subprocess import Popen, PIPE
import datetime
import time
import pymysql
from collections import Counter
import json


# Global Variables
semiColon = ":"
Originfpath = "/Users/mathiesj/desktop/JPWP81500218.mp4"
filename = os.path.basename(Originfpath)
print filename
baseFilename = os.path.splitext(filename)[0]
Destfpath = "/Users/mathiesj/Desktop/Crop_detect/videos/" + baseFilename + "_10secs.mp4"
DestfpathImage = "/Users/mathiesj/Desktop/Crop_detect/videos/" + baseFilename + "_10secs.jpg"


# FUNCTIONS
def GetDuration():
    print "Get duration of: %s" % Originfpath
    global info
    try:
        p = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "-sexagesimal", Originfpath, "-print_format", "json"]) # , "-show_streams", "-print_format", "json"
        info = json.loads(p)
        print info
        print info["format"]["duration"]
        global clipDuration
        global strDuration
        strDuration = info["format"]["duration"]
        videoTime = datetime.datetime.strptime(strDuration, "%H:%M:%S.%f").time()
        print "duration: %s" % videoTime
        calculateTime()
    except subprocess.CalledProcessError:
        print "ffprobe error"


def calculateTime():
        strDuration = info["format"]["duration"]
        stop = "."
        strDuration1 = strDuration.split(stop,1)[0]
        print strDuration1
        hour = strDuration1[:1]
        minute = strDuration1.split(semiColon,2)[1]
        second = strDuration1.split(semiColon,2)[2]
        print hour
        print minute
        print second
        intMinute = int(minute) - 1
        intSecond = int(second) + 10
        global inPoint
        global outPoint
        if intMinute <= 9 and intSecond <= 59: # Clip is smaller than 9 minutes and smaller than 59 seconds
            inPoint = str(0) + hour + semiColon + str(0) + str(intMinute) + semiColon + second + stop + str(0)
            outPoint = str(0) + hour + semiColon + str(0) + str(intMinute) + semiColon + str(intSecond) + stop + str(0)
            print "In Point : %s" % inPoint
            print "Out Point : %s" % outPoint
            ClipAndEncode()
        elif intMinute >= 10 and intSecond <= 59: # Clip is larger than 10 minutes and smaller than 59 seconds 
            inPoint = str(0) + hour + semiColon + str(intMinute) + semiColon + second + stop + str(0)
            outPoint = str(0) + hour + semiColon + str(intMinute) + semiColon + str(intSecond) + stop + str(0)
            print "In Point: %s" % inPoint
            print "Out Point: %s " % outPoint
            ClipAndEncode()
        elif intMinute <= 9 and intSecond >= 60: # Clip is smaller than 9 minutes and larger then 60 seconds 
            inPoint = str(0) + hour + semiColon + str(0) + str(intMinute) + semiColon + second + stop + str(0)
            outPoint = str(0) + hour + semiColon + str(0) + str(intMinute + 1) + semiColon + str(0) + str(intSecond - 60) + stop + str(0)
            print "In Point: %s" % inPoint
            print "Out Point: %s " % outPoint
            ClipAndEncode()
        elif intMinute >= 10 and intSecond >= 60: # Clip is larger than 10 minutes and larger than 60 seconds
            inPoint = str(0) + hour + semiColon + str(intMinute) + semiColon + second + stop + str(0)
            outPoint = str(0) + hour + semiColon + str(intMinute + 1) + semiColon + str(0) + str(intSecond - 60) + stop + str(0)
            print "In Point: %s" % inPoint
            print "Out Point: %s " % outPoint
            ClipAndEncode()
        else:
            print "time calculation error"






def ClipAndEncode():
    print "File to clip: %s " % Originfpath
    try:
        p = subprocess.Popen(["ffmpeg", "-i", Originfpath, "-ss", inPoint, "-t", "1", "-f", "image2", DestfpathImage], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = subprocess.Popen(["ffmpeg", "-i", Originfpath, "-ss", inPoint, "-to", outPoint, "-c", "copy", Destfpath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        infos = p.stderr.read()
        print infos
    except subprocess.CalledProcessError:
        print "ffmpeg error"



# Start 
GetDuration()







