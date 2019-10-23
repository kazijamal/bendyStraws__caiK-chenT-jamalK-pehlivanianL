import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="odyssey.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#==========================================================
