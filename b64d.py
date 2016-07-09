#! python

import sys
import os
import re
from base64 import b64decode as decode
import requests

regexp = re.compile(r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$")

def testifbase64(candidate):
	if re.match(regexp,candidate):
		print decode(candidate)
	else:
		print "Error, no valid Base64 detected, re-check your arguments! Exiting."
		sys.exit(-1)

def main():
	if len(sys.argv) < 2:
		print "[ Utility for decoding base64 ]"
		print "Jonathan James <jj@areusecure.se>\n"
		print "{} [Base64-string, file or URL]".format(sys.argv[0])
		sys.exit(0)

	file = sys.argv[1]

	if file.lower().startswith("http"):
		header = {}
		header["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
		r = requests.get(file,headers=header)
		if r.status_code == 200:
			r.encoding = "utf-8"
			testifbase64(r.content)

		elif r.status_code == 404:
			print "Error, URL returned 404 (not found) for {}".format(file)
		else:
			print "Server returned HTTP status code {}".format(r.status_code)

	elif os.path.isfile(file):
		with open(file,'rb') as f:
			data = f.read()
			testifbase64(data)
	else:
		testifbase64(file)

if __name__ == "__main__":
	main()