from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from database import db, User
from config import *

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
    # This custom validator can be replaced with the equivalent official one provided by WTForms, but not necessary
    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords must match.')
        
class FoodLogForm(FlaskForm):
    food_name = StringField('Enter a food item or meal', validators=[DataRequired(), Length(logInputMinLen, logInputMaxLen)])
    calories = IntegerField('Enter a calorie amount', validators=[DataRequired(), NumberRange(0)])
    submit = SubmitField('Log Food')

class SleepLogForm(FlaskForm):
    sleep_duration = IntegerField('Enter number of hours slept', validators=[DataRequired(), NumberRange(0)])
    sleep_quality = StringField('Enter sleep quality',  validators=[DataRequired(), Length(logInputMinLen, logInputMaxLen)])
    sleep_comment = StringField('Enter a comment',  validators=[DataRequired(), Length(logInputMinLen, logInputMaxLen)])
    submit = SubmitField('Log Sleep')

class HydrationLogForm(FlaskForm):
    fluid_type = StringField('Enter a fluid type', validators=[DataRequired(), Length(logInputMinLen, logInputMaxLen)])
    amount_ml = IntegerField('Enter the amount drank', validators=[DataRequired(), NumberRange(0)])
    caloric_val =  IntegerField('Enter caloric value', validators=[DataRequired(), NumberRange(0)])
    submit = SubmitField('Log Hydration')

class MedicationLogForm(FlaskForm):
    med_name = StringField('Enter a medication', validators=[DataRequired(), Length(logInputMinLen, logInputMaxLen)])
    amount_mg = IntegerField('Enter the amount taken (mg)', validators=[DataRequired(), NumberRange(0)])
    frequency =  StringField('Enter the frequency medication is taken', validators=[DataRequired(), Length(logInputMinLen, logInputMaxLen)])
    comment = StringField('Enter a comment (optional)', validators=[Length(0, logInputMaxLen)])
    submit = SubmitField('Log Medication')