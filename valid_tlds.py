import requests
# Retrieved the list from http://data.iana.org/TLD/tlds-alpha-by-domain.txt
tlds = ""
tlds += "tlds = ["
#with open('/Users/jj/Desktop/tlds.txt','r') as f:
f = requests.get("http://data.iana.org/TLD/tlds-alpha-by-domain.txt")
for line in f.iter_lines():
	if "#" not in line:
		tlds += ("," + "'" + line.strip() + "'")
tlds += "]"
print tlds.lower()