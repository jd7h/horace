import urllib
import json
import csv
import os.path

# load the apikey
with open("apikey.json") as f:
	API_KEY = json.load(f)

baseurl = "http://isbndb.com/api/v2/json/%s/" %API_KEY

# try to open the existing list of books
if os.path.exists("books.json"):
	with open("books.json") as f:
		books = json.load(f)
else:
	books = {}


nr_added = 0
# open csv with isbn number to add to the list
with open("../data/test.csv", 'rb') as f:
	reader = csv.reader(f,delimiter=';')
	for row in reader:
		if row[0] in books:
			continue
		bookinfo = json.load(urllib.urlopen(baseurl+"book/"+row[0]))
		if "error" in bookinfo: 
			print "[Error] "+bookinfo["error"]
			continue
		item = bookinfo["data"][0]
		authorlist = []
		for auth in item["author_data"]:
			authorlist.append(auth["name"])
		librarybook = dict(title=item["title"],authors=authorlist,available=True)
		books[row[0]] = librarybook
		nr_added += 1

print "%s books were added to the list." %nr_added
towrite = json.dumps(books)

with open("books.json",'wb') as f:
	f.write(towrite)
