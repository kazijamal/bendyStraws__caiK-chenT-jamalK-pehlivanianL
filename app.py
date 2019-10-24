from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os
from utl import dbfunctions, dbeditfunctions, dbcreatefunctions

app = Flask(__name__)

app.secret_key = os.urandom(32)

DB_FILE = "odyssey.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitate db operations
dbfunctions.createTables(c)

storyID = 1

def checkAuth():
    if "userID" in session:
        return True
    else:
        return False

@app.route("/")
def root():
    if checkAuth(): #if you've already logged in
        return redirect("/welcome")
    else: #if not, redirect to login page
        return redirect("/login")

@app.route("/login") #login page
def login():
    if checkAuth(): #if you're already logged in
        return redirect('/welcome') #else load the login template
    return render_template('login.html')

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
        return redirect(url_for('welcome'))

@app.route("/logout")
def logout():
    session.pop('userID')
    session.pop('username')
    return redirect(url_for('root'))

@app.route("/welcome")
def welcome():
    if checkAuth():
        return render_template('welcome.html')
    else:
        return render_template('login.html')

#page for creating a new story
@app.route("/createstory")
def createStory():
    if checkAuth():
        return render_template("createstory.html")
    else: return render_template('login.html')

#route for creating a new story
@app.route("/newstory", methods=['POST'])
def newStory():
    title = request.form['title']
    content = request.form['content']
    userID = session['userid']
    storyID = dbcreatefunctions(c, storyID, title, content, userID)
    return redirect("/story/{}".format(storyID))

if __name__ == "__main__":
    app.debug = True
    app.run()
dbeditfunctions.debugAdd(c);
db.commit()
db.close()
