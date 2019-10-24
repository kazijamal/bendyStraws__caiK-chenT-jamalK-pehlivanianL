from utl import dbcreatefunctions,dbfunctions

#EDIT STORIES
def addToStory(c, storyID, userID,content):
    c.execute("INSERT INTO story_edits VALUES (?, ?, ?, NULL)", (storyID, userID, content))


def getContributedStories(c, userID):
    c.execute("SELECT storyID FROM story_edits WHERE userID = "+str(userID))
    return c.fetchall()


def getNotContributedStories(c, userID):
    #c.execute("SELECT stories.storyID, userID \n FROM stories \nLEFT JOIN story_edits WHERE userID = "+str(userID)+" USING(storyID) \nWHERE userID IS NULL")
    return c.fetchall()

# DEBUG:
def debugAdd(c):
    dbcreatefunctions.createStory(c,"HelloWorld","hi",0)
    dbcreatefunctions.createStory(c,"HelloWorxd","hi",5)
    addToStory(c,1," world", 5)
    dbfunctions.debugPrintSelect(c,"story_edits")
    print(str(getContributedStories(c,5)))
    print(str(getNotContributedStories(c,5)))
