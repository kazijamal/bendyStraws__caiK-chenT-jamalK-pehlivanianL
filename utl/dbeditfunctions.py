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
