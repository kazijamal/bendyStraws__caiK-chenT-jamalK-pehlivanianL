import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE="odyssey.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#==========================================================

c.execute("DROP TABLE IF EXISTS stories");
c.execute("CREATE TABLE IF NOT EXISTS stories (storyID INTEGER PRIMARY KEY, name TEXT)");

c.execute("DROP TABLE IF EXISTS story_edits");
c.execute("CREATE TABLE IF NOT EXISTS story_edits (storyID INTEGER, userID INTEGER, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)");

c.execute("DROP TABLE IF EXISTS users");
c.execute("CREATE TABLE IF NOT EXISTS users (userID INTEGER, username TEXT, password TEXT)");

#==========================================================
storyID = 1

def createStory(title, content, userID):
    #create new record in stories table
    c.execute("INSERT INTO stories VALUES (NULL, ?)", (title, ))

    #create new record in story_edits TABLE
    c.execute("INSERT INTO story_edits VALUES (?, ?, ?, NULL)", (storyID, userID, content))

    storyId = storyID + 1

createStory("title", "this is the content of the story", 5)

#==========================================================

db.commit()
db.close()
