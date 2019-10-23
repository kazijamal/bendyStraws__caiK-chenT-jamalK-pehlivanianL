import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="odyssey.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#==========================================================

c.execute("DROP TABLE IF EXISTS stories");
c.execute("CREATE TABLE IF NOT EXISTS stories (id INTEGER, name TEXT)");

c.execute("DROP TABLE IF EXISTS story-edits");
c.execute("CREATE TABLE IF NOT EXISTS story-edits (storyID INTEGER, userID INTEGER, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)");

c.execute("DROP TABLE IF EXISTS users");
c.execute("CREATE TABLE IF NOT EXISTS users (userID INTEGER, username TEXT, password, TEXT)");

#=========================================================

storyID = 0

def createStory(title, text, userID):
    #create new record in stories table
    c.execute("INSERT INTO stories values(%d,'%s')", % (storyID, title))

    #create new record in story_edits TABLE
    c.execute("INSERT INTO story_edits values(%d, %d, '%s')", %(storyID, userID, text))

    #increment storyID
    storyID = storyID + 1
