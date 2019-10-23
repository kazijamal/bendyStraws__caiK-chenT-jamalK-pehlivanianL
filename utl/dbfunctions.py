def createTables(c):
    c.execute("DROP TABLE IF EXISTS stories");
    c.execute("CREATE TABLE IF NOT EXISTS stories (storyID INTEGER PRIMARY KEY, name TEXT)");

    c.execute("DROP TABLE IF EXISTS story_edits");
    c.execute("CREATE TABLE IF NOT EXISTS story_edits (storyID INTEGER, userID INTEGER, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)");

    c.execute("DROP TABLE IF EXISTS users");
    c.execute("CREATE TABLE IF NOT EXISTS users (userID INTEGER, username TEXT, password TEXT)");
    
#EDIT STORIES
def addToStory(c, storyID, content, userID):
    c.execute("INSERT INTO story_edits VALUES (?, ?, ?, NULL)", (storyID, userID, content))


def getContributedStories(c, userID):
    c.execute("SELECT storyID FROM story_edits WHERE userID = "+str(userID))
    return c.fetchall()


def getNotContributedStories(c, userID):
    #c.execute("SELECT stories.storyID, userID \n FROM stories \nLEFT JOIN story_edits WHERE userID = "+str(userID)+" USING(storyID) \nWHERE userID IS NULL")
    return c.fetchall()

def createStory(c, title, content, userID):
    global storyID
    #create new record in stories table
    c.execute("INSERT INTO stories VALUES (NULL, ?)", (title, ))

    #create new record in story_edits TABLE
    addToStory(storyID, content, userID)
    storyID += 1
    
# DEBUG:
def debugAdd():
    createStory("HelloWorld","hi",0)
    addToStory(2," world", 5)
    debugPrintSelect("story_edits")
    print(str(getContributedStories(5)))
    print(str(getNotContributedStories(5)))
    
def debugPrintSelect(c, table):
    c.execute("SELECT * FROM "+table)
    print(str(c.fetchall()) + "\n")
