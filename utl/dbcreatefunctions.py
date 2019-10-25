from utl import dbeditfunctions
storyID = 1
def createStory(c, title, userID, content):
    global storyID
    c.execute("INSERT INTO stories VALUES (NULL, ?)", (title, ))
    dbeditfunctions.addToStory(c,storyID, userID, content)
    storyID += 1
    return storyID
