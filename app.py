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
        return redirect('/home')
    return render_template('signup.html')

@app.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    if password != password2:
        flash("Passwords do not match")
        return redirect(url_for('signup'))
    else:
        c.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, password))
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
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route("/story/<storyID>")
def readStory(storyID):
    if checkAuth():
        if dbfunctions.getMaxStoryID(c) == None or int(storyID) < 1 or int(storyID) > dbfunctions.getMaxStoryID(c):
            flash("Invalid story ID")
            return redirect(url_for('home'))
        else:
            title = dbfunctions.selectStory(c, storyID)[0][0]
            edits = dbfunctions.getStoryEdits(c, storyID)
            return render_template('story.html', title=title, edits=edits)
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
    dbcreatefunctions.createStory(c, storyID, title, content, userID, username)
    return redirect('/story/{}'.format(storyID))

if __name__ == "__main__":
    app.debug = True
    app.run()

dbeditfunctions.debugAdd(c);
db.commit()
db.close()
