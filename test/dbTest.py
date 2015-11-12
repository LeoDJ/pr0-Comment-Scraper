import sqlite3
dbPath = 'db.sqlite'
conn = sqlite3.connect(dbPath)
with conn:
	db = conn.cursor()
	data2=[(5013232, 890083, 0,       1436710549, 'Deiner?',       'Neu',          3, 0), 
		   (5013262, 890083, 5013232, 1436710670, 'Leider nicht.', 'InkOgNitO666', 3, 0)]
	db.executemany("INSERT INTO comments VALUES (?,?,?,?,?,?,?,?)", data2)