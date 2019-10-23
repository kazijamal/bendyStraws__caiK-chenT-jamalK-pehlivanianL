def createTables(c):
    c.execute("DROP TABLE IF EXISTS stories");
    c.execute("CREATE TABLE IF NOT EXISTS stories (storyID INTEGER PRIMARY KEY, name TEXT)");

    c.execute("DROP TABLE IF EXISTS story_edits");
    c.execute("CREATE TABLE IF NOT EXISTS story_edits (storyID INTEGER, userID INTEGER, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)");

    c.execute("DROP TABLE IF EXISTS users");
    c.execute("CREATE TABLE IF NOT EXISTS users (userID INTEGER, username TEXT, password TEXT)");
   

def createStory(c, title, content, userID):
    global storyID
    #create new record in stories table
    c.execute("INSERT INTO stories VALUES (NULL, ?)", (title, ))

    #create new record in story_edits TABLE
    addToStory(storyID, content, userID)
    storyID += 1
    
def debugPrintSelect(c, table):
    c.execute("SELECT * FROM "+table)
    print(str(c.fetchall()) + "\n")
