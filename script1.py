# Importing the Flask object from the flask library
from flask import Flask, render_template

# Instantiating the Flask class using the app object
app=Flask(__name__)
# __name__ is a special variable you get for the name of the python script

@app.route('/')
def home(): # defines what our web home page will do
    return render_template("home.html")

@app.route('/about/')
def about(): # defines what our web home page will do
    return render_template("about.html")

@app.route('/projects/')
def projects(): # defines what our web home page will do
    return render_template("projects.html")

# When you execite the script, python assigns the name __main__
if __name__ == "__main__":
    app.run(debug=True) # Would not be executed if the script was imported from somewhere else
