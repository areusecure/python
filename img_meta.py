# -*- coding: utf-8 -*-

import sys, os
import hashlib
import pdb
from PIL import Image
from PIL.ExifTags import TAGS

#Hash
f = open(sys.argv[1])
h = hashlib.sha1()
h.update(f.read())
hash = h.hexdigest()
f.close()
# End hash

i = Image.open(sys.argv[1])
info = i._getexif()
exif={}
for tag, value in info.items():
	decoded = TAGS.get(tag,tag)
	exif[decoded]=value

GPS = exif['GPSInfo']
Tid = exif['DateTimeOriginal']
Tillverkare = exif['Make']
Modell = exif['Model']
Mjukvaruversion = exif['Software']

latData = GPS[2]
lonData = GPS[4]

latDeg = latData[0][0]/float(latData[0][1])
latMin = latData[1][0]/float(latData[1][1])
latSec = latData[2][0]/float(latData[2][1])
lonDeg = lonData[0][0]/float(lonData[0][1])
lonMin = lonData[1][0]/float(lonData[1][1])
lonSec = lonData[2][0]/float(lonData[2][1])

Lat = (latDeg + (latMin + latSec/60.0)/60.0)
if GPS[1] == 'S': Lat = -Lat
Lon = (lonDeg + (lonMin + lonSec/60.0)/60.0)
if GPS[3] == 'W': Lon = -Lon

print "Filnamn: " + sys.argv[1]
print "SHA1: " + hash
print "Taget med en " + Tillverkare + " " + Modell + "(Version: " + Mjukvaruversion + ")"
print "Datum och tid: " + Tid
print "GPS-koordinater: " + str(Lat) + ","+str(Lon)
