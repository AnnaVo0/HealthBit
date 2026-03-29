from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user
from user import User
from forms import LoginForm, RegisterForm
from app import db

main = Blueprint('main', __name__)

# Note: For future pages that require the user to be logged in to view, use the @login_required decorator

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Note: db.session.execute() does not work for the below line, for some reason, do not use it for this query in particular
        user = User.query.filter_by(username = login_form.username.data, password = login_form.password.data).first()
        if user is not None:
            login_user(user, remember=login_form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        login_form.username.errors.append('')
        login_form.password.errors.append('The username and/or password you have entered is incorrect. Please try again.')
    return render_template('login.html', form = login_form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        # TO DO: PROPERLY HASH/ENCRYPT PASSWORD (possibly using flask bcrypt) FOR SECURITY BEFORE STORING IN DATABASE
        user = User(username=reg_form.username.data, password=reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form = reg_form)