#!/usr/bin/env python
# -*- coding: utf-8 -*-
# get_location.py - Part of Jonathan James's forensic toolkit for iPhone. http://jonathanj.com - jj@jonathanj.com
# Standalone usage: get_location.py [file] [limit] or get_location.py to set the standard values.

import time
import sys
from sqlite3 import dbapi2 as sql

class location_info:
	location_db = ""
	def __init__(self,dbfile):
		self.location_db = dbfile
	def list_gps(self,limit):
		rows = 0
		self.dbconnect()
		self.c.execute("select Timestamp, Latitude, Longitude from CellLocation limit %s;" % (limit))
		print "Row:\tTimestamp:\t\t\tLatitude:\tLongitude:"		
		for row in self.c:
			if len(row)==3:
				rows += 1
				floattime = float(row[0])
				ctime = time.ctime(floattime + 978328800)
				print "%s\t%s\t%s\t%s" % (rows,ctime,row[1],row[2])
	def list_gpswlan(self,limit):
		rows = 0
		self.dbconnect()
		self.c.execute("select MAC, Timestamp, Latitude, Longitude from WifiLocation limit %s;" % (limit))
		print "Row:\tBSSID:\t\t\tTimestamp:\t\t\tLatitude:\tLongitude:"
		for row in self.c:
			if len(row)==4:
				rows += 1
				floattime = float(row[1])
				ctime = time.ctime(floattime + 978328800)
				print "%s\t%s\t%s\t%s\t%s" % (rows, row[0], ctime, row[2], row[3])
	def dbconnect(self):
		self.db = sql.connect(self.location_db)
		self.c = self.db.cursor()	

if __name__ == '__main__':
	
	# Build our location_info object	
	if (len(sys.argv) > 1):
        	f=location_info(sys.argv[1])
	else:
        	f=location_info('/var/root/Library/Caches/locationd/consolidated.db')
	if (len(sys.argv) > 2):
        	limit = int(sys.argv[2])
	else:
        	limit = 100

	#List data from CellLocation table
	f.list_gps(limit)

	#List data from WifiLocation table
        f.list_gpswlan(limit)
