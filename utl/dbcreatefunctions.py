from utl import dbeditfunctions

def createStory(c, storyID, title, content, userID):
    c.execute("INSERT INTO stories VALUES (NULL, ?)", (title, ))
    dbeditfunctions.addToStory(c, storyID, content, userID);
    return storyID + 1
