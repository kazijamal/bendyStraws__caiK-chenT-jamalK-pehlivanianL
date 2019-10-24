from utl import dbeditfunctions
storyID = 0
def createStory(c, title, content, userID):
    global storyID
    c.execute("INSERT INTO stories VALUES (NULL, ?)", (title, ))
    dbeditfunctions.addToStory(c,storyID, userID,content)
    return storyID + 1
