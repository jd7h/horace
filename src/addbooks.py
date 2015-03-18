import json
import requests
import csv
import os.path
import logging

logging.basicConfig(filename='horace.log',
	level=logging.INFO,
	format='%(asctime)s %(levelname)s: %(message)s')

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
with open("../data/test.csv", 'rt') as f:
	reader = csv.reader(f,delimiter=';')
	for row in reader:
		if row[0] in books:
			continue
		r = requests.get(baseurl+"book/"+row[0])
		bookinfo = r.json()
		if "error" in bookinfo: 
			logging.error(bookinfo["error"])
			continue
		item = bookinfo["data"][0]
		authorlist = []
		for auth in item["author_data"]:
			authorlist.append(auth["name"])
		librarybook = dict(info=(dict(title=item["title"],authors=authorlist)),status=(dict(available=True,date=None,member=None)))
		books[row[0]] = librarybook
		print(row[0])
		nr_added += 1

#print("%s books were added to the list." %nr_added)
logging.info("%s books were added to the library", nr_added)
towrite = json.dumps(books)

with open("books.json",'wb') as f:
	f.write(towrite.encode('utf-8'))
	logging.info("Library updated.")
