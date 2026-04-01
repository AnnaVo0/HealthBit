'''
    HOW TO RUN:
    
    1. Run 'pip install -r requirements.txt' to download all current dependencies, activate venv if using one
    2. Run app.py using the command 'flask run'

'''
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'dev'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# serve locally for faster and offline development
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

from routes import main

app.register_blueprint(main)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)