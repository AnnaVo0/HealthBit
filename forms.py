from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from database import db, User
from config import usernameMinLen, usernameMaxLen, pwdMaxLen, pwdMinLen

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(usernameMinLen, usernameMaxLen)])
    password = PasswordField('Password', validators=[DataRequired(), Length(pwdMinLen, pwdMaxLen)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(usernameMinLen, usernameMaxLen)])
    password = PasswordField('Password', validators=[DataRequired(), Length(pwdMinLen, pwdMaxLen)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user = db.session.execute(db.select(User).filter_by(username=username.data)).first()
        if existing_user:
            raise ValidationError('The username you have entered already exists. Please re-enter a new one.')

    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords must match.')