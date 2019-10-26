from utl import dbcreatefunctions,dbfunctions

def getStoryEdits(c, storyID):
    c.execute("SELECT * FROM story_edits WHERE storyID = ? ORDER BY datetime(timestamp) DESC", (storyID, ))
    return c.fetchall()

#returns story's latest update. - a tuple
def getLatestStoryEdit(c, storyID):
    edits = getStoryEdits(c, storyID)
    return edits[-1]

#EDIT STORIES
def addToStory(c, storyID, userID, username, content):
    c.execute("INSERT INTO story_edits VALUES (?, ?, ?, ?, datetime('now'))", (storyID, userID, username, content))

#returns all the stories this user has edited (can Read)
def getStoriesEdited(c, userID):
    c.execute("SELECT * FROM stories where storyID IN (SELECT storyID FROM story_edits WHERE userID = ?)", (userID, ))
    return c.fetchall()

#returns all the stories this user has not edited (cannot Read)
def getStoriesNotEdited(c, userID):
    c.execute("SELECT * FROM stories where storyID NOT IN (SELECT storyID FROM story_edits WHERE userID = ?)", (userID, ))
    return c.fetchall()

def htmlStoriesNotEdited(c,userID):
    stories = "<center>"
    can_edit = getStoriesNotEdited(c,userID)
    for k,v in can_edit:
        stories += "<a href = /edit/"+k+">"
    return stories

def hasEdited(c,userID,storyID):
    c.execute("SELECT * FROM story_edits WHERE userID = ? AND storyID = ?", (userID, storyID))
    return c.fetchone() != None
# DEBUG:
def debugAdd(c):
    dbfunctions.dropTables(c)
    dbfunctions.createTables(c)
    dbcreatefunctions.createStory(c,1,"HelloWorld",0,"StrawBerry","hi")
    dbcreatefunctions.createStory(c,2,"HelloWorxd",0,"StrawBerry","test")
    addToStory(c,1,5,"TheLastStraw"," world")
    dbfunctions.debugPrintSelect(c,"story_edits")
    dbfunctions.debugPrintSelect(c,"stories")
    print(str(getStoriesEdited(c,5)))
    print(str(getStoriesNotEdited(c,5)))
    print(hasEdited(c,5,1))
