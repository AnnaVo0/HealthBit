from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from database import db, User, FoodEntry, SleepEntry, HydrationEntry, MedicationEntry, ExerciseEntry, \
    BowelMovementEntry, WeightEntry, UrineEntry
from forms import LoginForm, RegisterForm, FoodLogForm, SleepLogForm, HydrationLogForm, MedicationLogForm, \
    ExerciseLogForm, BowelLogForm, WeightLogForm, UrineLogForm
import bcrypt

main = Blueprint('main', __name__)

# Note: For future pages that require the user to be logged in to view, use the @login_required decorator

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()

    if reg_form.validate_on_submit():
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(reg_form.password.data.encode('utf-8'), salt)
        user = User(username=reg_form.username.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))

    return render_template('register.html', form=reg_form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        # Note: db.session.execute() does not work for the below line, for some reason, do not use it for this query in particular
        user = User.query.filter_by(username=login_form.username.data).first()
        
        if user and bcrypt.checkpw(login_form.password.data.encode('utf-8'), user.password):
            login_user(user, remember=login_form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        
        login_form.username.errors.append('')
        login_form.password.errors.append('The username and/or password you have entered is incorrect. Please try again.')
        
    return render_template('login.html', form=login_form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    #to get the count of each module entries on dashboard, so need to do this for other modules too
    food_count = FoodEntry.query.filter_by(user_id=current_user.id).count()
    sleep_count = SleepEntry.query.filter_by(user_id=current_user.id).count()
    hydration_count = HydrationEntry.query.filter_by(user_id=current_user.id).count()
    medication_count = MedicationEntry.query.filter_by(user_id=current_user.id).count()
    exercise_count = ExerciseEntry.query.filter_by(user_id=current_user.id).count()
    bowel_count = BowelMovementEntry.query.filter_by(user_id=current_user.id).count()
    weight_count = WeightEntry.query.filter_by(user_id=current_user.id).count()
    urine_count = UrineEntry.query.filter_by(user_id=current_user.id).count()
    return render_template('dashboard.html', food_count=food_count, sleep_count=sleep_count, hydration_count=hydration_count, medication_count=medication_count, exercise_count=exercise_count, bowel_count=bowel_count, weight_count=weight_count, urine_count=urine_count)

@main.route('/log-food', methods=['GET', 'POST'])
@login_required
def log_food():
    log_form = FoodLogForm()
    if log_form.validate_on_submit():
        food_name = request.form['food_name']
        calories = request.form['calories']
        log = FoodEntry(user_id=current_user.id, food_name=food_name, calories=calories)
        db.session.add(log)
        db.session.commit()

    food_logs = FoodEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('log_food.html', form=log_form, food_logs=food_logs)

@main.route('/log-sleep', methods=['GET', 'POST'])
def log_sleep():
    log_form = SleepLogForm()
    if log_form.validate_on_submit():
        sleep_duration = request.form['sleep_duration']
        sleep_quality = request.form['sleep_quality']
        sleep_comment = request.form['sleep_comment']
        log = SleepEntry(user_id=current_user.id, sleep_duration=sleep_duration, sleep_quality=sleep_quality, sleep_comment=sleep_comment)
        db.session.add(log)
        db.session.commit()

    sleep_logs = SleepEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('log_sleep.html', form=log_form, sleep_logs=sleep_logs)


@main.route('/log-hydration', methods=['GET', 'POST'])
def log_hydration():
    log_form = HydrationLogForm()
    if log_form.validate_on_submit():
        fluid_type = request.form['fluid_type']
        amount_ml = request.form['amount_ml']
        caloric_val = request.form['caloric_val']
        log = HydrationEntry(user_id=current_user.id, fluid_type=fluid_type, amount_ml=amount_ml, caloric_val=caloric_val)
        db.session.add(log)
        db.session.commit()

    hydration_logs = HydrationEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('log_hydration.html', form=log_form, hydration_logs=hydration_logs)

@main.route('/log-medication', methods=['GET', 'POST'])
def log_medication():
    log_form = MedicationLogForm()
    if log_form.validate_on_submit():
        med_name = request.form['med_name']
        amount_mg = request.form['amount_mg']
        frequency = request.form['frequency']
        comment = request.form['comment']
        log = MedicationEntry(user_id=current_user.id, med_name=med_name, amount_mg=amount_mg, frequency=frequency, comment=comment)
        db.session.add(log)
        db.session.commit()

    medication_logs = MedicationEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('log_meds.html', form=log_form, medication_logs=medication_logs)


@main.route('/log-exercise', methods=['GET', 'POST'])
def log_exercise():
    log_form = ExerciseLogForm()
    if log_form.validate_on_submit():
        exercise_name = request.form['exercise_name']
        minutes = request.form['minutes']
        calories_burned = request.form['calories_burned']
        log = ExerciseEntry(user_id=current_user.id, exercise_name=exercise_name, minutes=minutes, calories_burned=calories_burned)
        db.session.add(log)
        db.session.commit()

    exercise_logs = ExerciseEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('log_exercise.html', form=log_form, exercise_logs=exercise_logs)


@main.route('/log-bowel', methods=['GET', 'POST'])
def log_bowel():
    log_form = BowelLogForm()
    if log_form.validate_on_submit():
        stool_type = request.form['stool_type']
        stool_color = request.form['stool_color']
        stool_description = request.form['stool_description']
        log = BowelMovementEntry(user_id=current_user.id, stool_type=stool_type, stool_color=stool_color, stool_description=stool_description)
        db.session.add(log)
        db.session.commit()

    bowel_logs = BowelMovementEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('log_bowel.html', form=log_form, bowel_logs=bowel_logs)

@main.route('/log-weight', methods=['GET', 'POST'])
def log_weight():
    log_form = WeightLogForm()
    if log_form.validate_on_submit():
        weight_lbs = request.form['weight_lbs']
        log = WeightEntry(user_id=current_user.id, weight_lbs=weight_lbs)
        db.session.add(log)
        db.session.commit()

    weight_logs = WeightEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('log_weight.html', form=log_form, weight_logs=weight_logs)

@main.route('/log-urine', methods=['GET', 'POST'])
def log_urine():
    log_form = UrineLogForm()
    if log_form.validate_on_submit():
        urine_color = request.form['urine_color']
        urine_comment = request.form['urine_comment']
        log = UrineEntry(user_id=current_user.id, urine_color=urine_color, urine_comment=urine_comment)
        db.session.add(log)
        db.session.commit()

    urine_logs = UrineEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('log_urine.html', form=log_form, urine_logs=urine_logs)