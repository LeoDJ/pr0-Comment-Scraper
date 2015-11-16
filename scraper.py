import sqlite3
import json
import urllib2
import os.path
import sys
import time

lastIDPath = 'lastID.txt'
dbPath = 'db.sqlite'

saveEvery=100


itemPage = 'http://pr0gramm.com/api/items/info?itemId='
homePage = 'http://pr0gramm.com/api/items/get?flags=7'

lastID=1
start = 1
end = 1

if not os.path.exists(dbPath):
	print "creating database... ",
	conn = sqlite3.connect(dbPath)
	db = conn.cursor()
	#db structure: Comment ID | Post ID | Parent Comment | Creation Time | Comment Text | User | Upvotes | Downvotes
	db.execute('''CREATE TABLE comments
				 (
				 commentID INT NOT NULL PRIMARY KEY, 
				 postID INT, 
				 parentID INT, 
				 time INT, 
				 text TEXT, 
				 user TEXT, 
				 up INT, 
				 down INT)''')
	print "done"
			 
conn = sqlite3.connect(dbPath)
db = conn.cursor()

def getLastID():
	if os.path.exists(lastIDPath):
		lastID = int(open(lastIDPath, 'r').read())
		print "Loaded last ID as", lastID
		return lastID
	else:
		return 0

def saveLastID():
	open(lastIDPath, 'w').write(str(lastID))
	print "Saved last ID as",lastID

def getMaxID():
	try:
		jsonItems = urllib2.urlopen(homePage).read()
		items = json.loads(jsonItems)
		maxID = items['items'][0]['id']
		print "Newest post is #" + str(maxID)
		return maxID
	except Exception as e:
		return 100000
	

def getData(id):
	rsp = urllib2.urlopen(itemPage + str(id))
	data = rsp.read()
	return data
	

def saveData(jsonData, id):
	data = {}
	data = json.loads(jsonData)
	for com in data["comments"]:
		#exists = False     #obsolete now, becuase of INSERT IGNORE
		#for row in db.execute("SELECT commentID FROM comments WHERE commentID = ?",[com['id']]):
		#	exists = True
		#if not exists:
		
		db.execute("INSERT OR IGNORE INTO comments VALUES (?,?,?,?,?,?,?,?)", (com['id'], int(id), com['parent'], com['created'], com['content'], com['name'], com['up'], com['down']))

			

while True:

	if(len(sys.argv) == 1):	
		start = getLastID()+1
		end = getMaxID()
	elif(len(sys.argv) == 2):	
		start = int(sys.argv[1])
		end = getMaxID()
	elif (len(sys.argv) == 3):
		start = int(sys.argv[1])
		end = int(sys.argv[2])
	else:
		print "Wrong parameter count"
	print "Will save comments from post #"+str(start)+" to #"+str(end)


	postCounter = 0
	try:
		for i in range(start,end+1):
			lastTime = time.clock()
			print "Saving comments for post #" + str(i) + "... ",
			
			gotData = ""
			while (gotData == ""):
				try:
					gotData = getData(i)
				except KeyboardInterrupt:
					break;
				except:
					gotData = ""
					print("exception after getData")
			saveData(gotData,i)
			print "done in",
			print str(round(time.clock()-lastTime, 2))+"s"
			lastID = i
			postCounter+=1
			if postCounter >= saveEvery:
				conn.commit()
				saveLastID()
				postCounter=0
		conn.commit()
	except KeyboardInterrupt:
			pass

