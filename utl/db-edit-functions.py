from utl import dbfunctions
#EDIT STORIES
def addToStory(c, storyID, content, userID):
    c.execute("INSERT INTO story_edits VALUES (?, ?, ?, NULL)", (storyID, userID, content))


def getContributedStories(c, userID):
    c.execute("SELECT storyID FROM story_edits WHERE userID = "+str(userID))
    return c.fetchall()


def getNotContributedStories(c, userID):
    #c.execute("SELECT stories.storyID, userID \n FROM stories \nLEFT JOIN story_edits WHERE userID = "+str(userID)+" USING(storyID) \nWHERE userID IS NULL")
    return c.fetchall()

# DEBUG:
def debugAdd():
    dbfunctions.createStory("HelloWorld","hi",0)
    addToStory(2," world", 5)
    debugPrintSelect("story_edits")
    print(str(getContributedStories(5)))
    print(str(getNotContributedStories(5)))
