"""
    HOW TO RUN:

    1) Follow Flask installation guide, ensure virtual environment is active if you are using one
    (You can also use 'pip install -r requirements.txt' to download all dependencies from the requirements.txt file)

    2) Run the following command inside the project folder: 'flask run --debug'
    Note: Running 'flask run' automatically looks for app.py and runs it, to run another module/page make sure to specify its name using --app

    To edit HTML, make/modify an HTML template inside templates then use the Flask render_template() method to render it (unless you plan on just hard-coding HTML in directly)
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('app.html');