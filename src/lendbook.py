import json
import os
import sys
import getopt
import time
import logging

logging.basicConfig(filename='horace.log',
	level=logging.INFO,
	format='%(asctime)s %(levelname)s: %(message)s')

def usage():
	helpmessage =	"""
usage: python lendbooks.py [option] [arg]
options:
 -h      : displays this help message
--help   : same as -h
 -m name : the person you lend an item
--member : same as -m
 -b isbn : the isbn of the item you lend
--book   : same as -b"""
	print(helpmessage)

def main(argv):
	member = "Rincewind"
	book = 9781473200265

	try:
		opts, args = getopt.getopt(argv, "hm:b:", ["help", "member=", "book="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-m", "--member"):
			member = arg
		elif opt in ("-b", "--book"):
			book = arg

	if os.path.exists("books.json"):
		with open("books.json") as f:
			library = json.load(f)
	else:
		#print("[Error] Couldn't find books.json")
		logging.error("Couldn't locate file books.json")
		sys.exit(2)

	if book in library:
		if library[book]['status']['available']:
			library[book]['status']['available'] = False
			library[book]['status']['member'] = member
			library[book]['status']['date'] = time.strftime("%x")
			logging.info("LOAN %s (%s) to %s", library[book]['info']['title'], book, member)
		else:
			#print("[ERROR] book %s is not available" %book)
			logging.error("Book %s is not available", book)
			sys.exit(2)
	else:
		#print("[Error] book %s not found in library" %book)
		logging.error("Book %s not found in library", book)

	updated_library = json.dumps(library)

	with open("books.json",'wb') as f:
		f.write(updated_library.encode('utf-8'))
		logging.info("Updated library file")



if __name__ == "__main__":
	main(sys.argv[1:])
