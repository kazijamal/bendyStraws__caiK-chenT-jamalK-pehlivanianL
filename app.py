from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os
from utl import dbfunctions, dbeditfunctions, dbcreatefunctions

app = Flask(__name__)

app.secret_key = os.urandom(32)

DB_FILE = "odyssey.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitate db operations
dbfunctions.createTables(c)

def checkAuth():
    if "userID" in session:
        return True
    else:
        return False

@app.route("/")
def root():
    if checkAuth(): #if you've already logged in
        return redirect(url_for('home'))
    else: #if not, redirect to login page
        return redirect(url_for('login'))

@app.route("/login") #login page
def login():
    if checkAuth():
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route("/signup") #signup page
def signup():
    if checkAuth():
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    c.execute("SELECT username FROM users WHERE username = ?", (username, ))
    a = c.fetchone()
    if a != None:
        flash("Account with that username already exists")
        return redirect(url_for('signup'))
    elif password != password2:
        flash("Passwords do not match")
        return redirect(url_for('signup'))
    elif len(password) < 8:
        flash("Password must be at least 8 characters in length")
        return redirect(url_for('signup'))

    else:
        c.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, password))
        db.commit()
        flash("Successfuly created user")
        return redirect(url_for('login'))

@app.route("/auth", methods=["POST"])
def auth():
    username = request.form['username']
    password = request.form['password']
    c.execute("SELECT userID, password FROM users WHERE username = ?", (username, ))
    a = c.fetchone()
    if a == None:
        flash("No user found with given username")
        return redirect(url_for('login'))
    elif password != a[1]:
        flash("Incorrect password")
        return redirect(url_for('login'))
    else:
        session['userID'] = a[0]
        session['username'] = username
        flash("Welcome " + username + ". You have been logged in successfully.")
        return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.pop('userID')
    session.pop('username')
    return redirect(url_for('root'))

@app.route("/home")
def home():
    if checkAuth():
        storiesEdited = dbeditfunctions.getStoriesEdited(c,session['userID'])
        storiesNotEdited = dbeditfunctions.getStoriesNotEdited(c,session['userID'])
        print(storiesEdited)
        print(storiesNotEdited)
        return render_template('home.html', storiesEdited=storiesEdited, storiesNotEdited=storiesNotEdited)
    else:
        return redirect(url_for('login'))

@app.route("/search")
def search():
    if checkAuth():
        query = request.args['query']
        response = dbfunctions.getSearch(c, query)
        storiesEdited = dbeditfunctions.getStoriesEdited(c,session['userID'])
        ids = []
        for story in storiesEdited:
            ids.append(story[0])
        stories = []
        for story in response:
            if story[0] in ids:
                stories.append(story + ("edited",))
            else:
                stories.append(story + ("unedited",))
        return render_template('search.html', query=query, stories=stories)
    else:
        return redirect(url_for('login'))

@app.route("/story/<storyID>")
def readStory(storyID):
    if checkAuth():
        # if no stories have been created or this story# is too high (not created)
        if dbfunctions.getMaxStoryID(c) == None or int(storyID) < 1 or int(storyID) > dbfunctions.getMaxStoryID(c):
            flash("Invalid story ID")
            return redirect(url_for('home'))
        else:
            title = dbfunctions.selectStory(c, storyID)[0]
            edits = dbeditfunctions.getStoryEdits(c, storyID)
            # print(edits)
            return render_template('story.html', title=title, edits=edits)
    else:
        return redirect(url_for('login'))

@app.route("/uneditedstories")
def uneditedStories():
    if checkAuth():
        storiesNotEdited = dbeditfunctions.getStoriesNotEdited(c,session['userID'])
        return render_template('uneditedstories.html', storiesNotEdited=storiesNotEdited)
    else:
        return redirect(url_for('login'))

@app.route("/edit/<storyID>")
def editStory(storyID):
    if checkAuth():
        # if no stories have been created or this story# is too high (not created)
        if dbfunctions.getMaxStoryID(c) == None or int(storyID) < 1 or int(storyID) > dbfunctions.getMaxStoryID(c):
            flash("Invalid story ID")
            return redirect(url_for('home'))
        else:
            if(dbeditfunctions.hasEdited(c,session['userID'],storyID)):
                flash("Already edited story")
                return redirect(url_for('home'))
            title = dbfunctions.selectStory(c, storyID)[0]
            edit = dbeditfunctions.getLatestStoryEdit(c, storyID)
            return render_template('edit.html', title=title, edit=edit)
    else:
        return redirect(url_for('login'))

#page for creating a new story
@app.route("/createstory")
def createStory():
    if checkAuth():
        return render_template('createstory.html')
    else:
        return redirect(url_for('login'))

#route for creating a new story
@app.route("/newstory", methods=['POST'])
def newStory():
    title = request.form['title']
    content = request.form['content']
    userID = int(session['userID'])
    username = session['username']
    if dbfunctions.getMaxStoryID(c) == None:
        storyID = 1
    else:
        storyID = dbfunctions.getMaxStoryID(c) + 1
    dbcreatefunctions.createStory(c, storyID, title, userID, username, content)
    db.commit()
    return redirect('/story/{}'.format(storyID))

if __name__ == "__main__":
    app.debug = True
    app.run()

# dbeditfunctions.debugAdd(c);
db.commit()
db.close()
