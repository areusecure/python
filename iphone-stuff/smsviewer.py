#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import time
from sqlite3 import dbapi2 as sql

sms_db = '/var/mobile/Library/SMS/sms.db'
add_db = '/var/mobile/Library/AddressBook/AddressBook.sqlitedb'
class iphone_forensics:
	db = ""
	c = ""
	def list_names(self):
		self.dbconnect(add_db)
		self.c.execute("select First, Last from ABPerson;")
		print "Names (First Last):"
		for row in self.c:
			if row[0] and row[1]:
				print row[0].encode('iso-8859-1') + " " + row[1].encode('iso-8859-1')
				print ""
	def get_name(address):
		self.dbconnect(add_db)
		#sql = "select First,Last where "
		#self.c.execute("s")
	def message_read(self, flags):
		return (int(flags) & 0x02) >> 1
	def list_sms(self):
		self.dbconnect(sms_db)
		self.c.execute("select * from message;")
		for row in self.c:
	        	print "ID: " + str(row[0])
			print "Avsändare: " + str(row[1])
			print "Date: " + time.ctime(row[2]) + " ctime(" + str(row[2]) + ")"
			if row[3]:
				print "Text: " + str(row[3].encode('iso-8859-1'))
			else:
				print "Text: [No Text]"
			print "Flags: " + str(row[4])
			print "Replace: " + str(row[5])
			print "Svc_center: " + str(row[6])
			print "Group ID: " + str(row[7])
			print "Association ID: " + str(row[8])
			print "Height: " + str(row[9])
			print "UIFlags: " + str(row[10])
			print "Version: " + str(row[11])
			print "Subject: " + str(row[12])
			print "Country: " + str(row[13])
			print "Headers: " + str(row[14])
			print "Recipients: " + str(row[15])
			print "Read: " + str(row[16])
			print ""
			print "---------------------------"
			print ""
	def next_sms_id(self):
		self.dbconnect(sms_db)
		self.c.execute("select ROWID from message order by ROWID desc;")
		return int(self.c.fetchone()[0])+1
	def dbconnect(self,db_file):
		self.db = sql.connect(db_file)
		self.c = self.db.cursor()	
 	def add_sms(self,src,dest,message,read):
		print "Adding sms"
		self.dbconnect(sms_db)
		print "Highest ID: " + str(self.next_sms_id())
		self.db.create_function('read', 1, self.message_read)
		sql = "insert into message(ROWID, address, text, read) values(%d,'%s','%s',%d)" % (f.next_sms_id(), src, message, read)
		print "SQL: " + sql
		self.c.execute(sql)
		print "ID: "
		print "From: " + src 
		print "Message: " + message
		self.db.commit()

f = iphone_forensics()
f.list_sms()
f.list_names()
