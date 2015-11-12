import sqlite3 as lite
import sys

cars = (
	(1, 'Audi', 52642),
	(2, 'Mercedes', 57127),
	(3, 'Skoda', 9000),
	(4, 'Volvo', 29000),
	(5, 'Bentley', 350000),
	(6, 'Hummer', 41400),
	(7, 'Volkswagen', 21600)
)


con = lite.connect('test.sqlite')
with con:
	cur = con.cursor()	  

	data2=[(5013232, 890083, 0,		  1436710549, 'Deiner?',	   'Neu',		   3, 0), 
		   (5013262, 890083, 5013232, 1436710670, 'Leider nicht.', 'InkOgNitO666', 3, 0)]
	cur.executemany("INSERT INTO comments VALUES (?,?,?,?,?,?,?,?)", data2)