from utl import dbeditfunctions
storyID = 0;
def createStory(c, title, content, userID):
    c.execute("INSERT INTO stories VALUES (NULL, ?)", (title, ))
    dbeditfunctions.addToStory(c,storyID, content, userID);
    return storyID + 1
