'''
    HOW TO RUN:
    
    1. Run 'pip install -r requirements.txt' to download all current dependencies, activate venv if using one
    2. Run app.py using the python command

'''
from enum import Enum
from flask import Flask, render_template, request, flash, redirect, url_for
from markupsafe import Markup
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired, Length, ValidationError, Regexp
from wtforms.fields import *
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5, SwitchField
from flask_login import LoginManager, UserMixin, login_user

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

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Should probably move the below classes and some other stuff to their own file(s)
usernameMinLen = 1
usernameMaxLen = 20
pwdMinLen = 8
pwdMaxLen = 150

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(usernameMinLen, usernameMaxLen)])
    password = PasswordField('Password', validators=[DataRequired(), Length(pwdMinLen, pwdMaxLen)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(usernameMinLen, usernameMaxLen)])
    password = PasswordField('Password', validators=[DataRequired(), Length(pwdMinLen, pwdMaxLen)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user = db.session.execute(db.select(User).filter_by(username = username.data)).first()
        if existing_user:
            raise ValidationError('The username you have entered already exists. Please re-enter a new one.')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(usernameMaxLen), nullable=False, unique=True)
    password = db.Column(db.String(pwdMaxLen), nullable=False)

with app.app_context():
    db.create_all()

# Note: For future pages that require the user to be logged in to view, use the @login_required decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Note: db.session.execute() does not work for the below line, for some reason, do not use it for this query in particular
        user = User.query.filter_by(username = login_form.username.data, password = login_form.password.data).first()
        if user is not None:
            login_user(user, remember=login_form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        login_form.username.errors.append('')
        login_form.password.errors.append('The username and/or password you have entered is incorrect. Please try again.')
    return render_template('login.html', form = login_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        # TO DO: PROPERLY HASH/ENCRYPT PASSWORD (possibly using flask bcrypt) FOR SECURITY BEFORE STORING IN DATABASE
        user = User(username=reg_form.username.data, password=reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form = reg_form)

if __name__ == '__main__':
    app.run(debug=True)