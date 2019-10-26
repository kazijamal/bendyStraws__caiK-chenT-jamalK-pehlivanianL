from utl import dbcreatefunctions,dbfunctions

#EDIT STORIES
def addToStory(c, storyID, userID, username, content):
    c.execute("INSERT INTO story_edits VALUES (?, ?, ?, ?, datetime('now'))", (storyID, userID, username, content))


def getContributedStories(c, userID):
    c.execute("SELECT storyID FROM story_edits WHERE userID = "+str(userID))
    return c.fetchall()


def getNotContributedStories(c, userID):
    #c.execute("SELECT stories.storyID, userID \n FROM stories \nLEFT JOIN story_edits WHERE userID = "+str(userID)+" USING(storyID) \nWHERE userID IS NULL")
    return c.fetchall()

# DEBUG:
def debugAdd(c):
    dbfunctions.dropTables(c)
    dbfunctions.createTables(c)
    dbcreatefunctions.createStory(c,1,"HelloWorld",0,"hi")
    dbcreatefunctions.createStory(c,2,"HelloWorxd",0,"test")
    addToStory(c,1,5," world")
    dbfunctions.debugPrintSelect(c,"story_edits")
    dbfunctions.debugPrintSelect(c,"stories")
    print(str(getContributedStories(c,5)))
    print(str(getNotContributedStories(c,5)))
