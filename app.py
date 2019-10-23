from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route("/")
def root():
    if "in" in session: #if you've already logged in
        return redirect("/welcome")
    else: #if not, redirect to login page
        return redirect("/login")

@app.route("/login") #login page
def login():
    if "in" in session: #if you're already logged in
        return redirect('/welcome') #else load the login template
    return render_template('login.html')

@app.route("/welcome")
def welcome():
    if "in" in session: #if you're already logged in
        return redirect('/welcome')
    else:
        return render_template('login.html') #else load the login template

# page for creating a new story
@app.route("/createstory")
def createStory():
    return render_template("createstory.html")

# route for creating a new story
@app.route("/newstory", methods=['POST'])
def newStory():
    return "new story route"

if __name__ == "__main__":
    app.debug = True
    app.run()
