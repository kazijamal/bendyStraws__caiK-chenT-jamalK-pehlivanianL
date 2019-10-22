from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return __name__;

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
