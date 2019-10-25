from utl import dbeditfunctions
def createStory(c, storyID, title, content, userID, username):
    c.execute("INSERT INTO stories VALUES (NULL, ?)", (title, ))
    dbeditfunctions.addToStory(c, storyID, userID, username, content)
