from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime, time, timezone
from database import db, User, FoodEntry, SleepEntry, HydrationEntry, MedicationEntry, ExerciseEntry, \
    BowelMovementEntry, WeightEntry, UrineEntry, HiddenModule
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
    hidden = [m.module_name for m in HiddenModule.query.filter_by(user_id=current_user.id).all()]

    #to get the count of each module entries on dashboard, so need to do this for other modules too
    food_count = FoodEntry.query.filter_by(user_id=current_user.id).count()
    sleep_count = SleepEntry.query.filter_by(user_id=current_user.id).count()
    hydration_count = HydrationEntry.query.filter_by(user_id=current_user.id).count()
    medication_count = MedicationEntry.query.filter_by(user_id=current_user.id).count()
    exercise_count = ExerciseEntry.query.filter_by(user_id=current_user.id).count()
    bowel_count = BowelMovementEntry.query.filter_by(user_id=current_user.id).count()
    weight_count = WeightEntry.query.filter_by(user_id=current_user.id).count()
    urine_count = UrineEntry.query.filter_by(user_id=current_user.id).count()
    return render_template('dashboard.html', food_count=food_count, sleep_count=sleep_count,
                           hydration_count=hydration_count, medication_count=medication_count, exercise_count=exercise_count,
                           bowel_count=bowel_count, weight_count=weight_count, urine_count=urine_count, hidden=hidden)

@main.route('/log-food', methods=['GET', 'POST'])
@login_required
def log_food():
    log_form = FoodLogForm()
    date_str = request.args.get('date') or date.today().isoformat()
    
    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        selected_date = datetime.fromisoformat(date_str).date()
    
    if request.method == 'GET':
        log_form.timestamp.data = datetime.combine(selected_date, datetime.now().time())
    
    if log_form.validate_on_submit():
        timestamp = log_form.timestamp.data.replace(tzinfo=timezone.utc)
        food_name = log_form.food_name.data
        calories = log_form.calories.data
        
        log = FoodEntry(user_id=current_user.id, food_name=food_name, calories=calories, timestamp=timestamp)
        db.session.add(log)
        db.session.commit()
        
        return redirect(url_for('main.log_food', date=log_form.timestamp.data.date().isoformat()))
    
    start = datetime.combine(selected_date, time.min, tzinfo=timezone.utc)
    end = datetime.combine(selected_date, time.max, tzinfo=timezone.utc)

    food_logs = current_user.get_food_entries(start_date=start, end_date=end)
    return render_template('log_food.html', form=log_form, food_logs=food_logs, selected_date=selected_date.isoformat())
@main.route('/log-sleep', methods=['GET', 'POST'])
@login_required
def log_sleep():
    log_form = SleepLogForm()
    if log_form.validate_on_submit():
        sleep_duration = log_form.sleep_duration.data
        sleep_quality = log_form.sleep_quality.data
        sleep_comment = log_form.sleep_comment.data
        log = SleepEntry(user_id=current_user.id, sleep_duration=sleep_duration, sleep_quality=sleep_quality, sleep_comment=sleep_comment)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('main.log_sleep'))

    sleep_logs = current_user.get_sleep_entries()
    return render_template('log_sleep.html', form=log_form, sleep_logs=sleep_logs)

@main.route('/log-hydration', methods=['GET', 'POST'])
@login_required
def log_hydration():
    log_form = HydrationLogForm()
    date_str = request.args.get('date') or date.today().isoformat()
    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        selected_date = datetime.fromisoformat(date_str).date()
    
    if request.method == 'GET':
        log_form.timestamp.data = datetime.combine(selected_date, datetime.now().time())
    
    if log_form.validate_on_submit():
        timestamp = log_form.timestamp.data.replace(tzinfo=timezone.utc)
        fluid_type = log_form.fluid_type.data
        amount_ml = log_form.amount_ml.data
        caloric_val = log_form.caloric_val.data
        log = HydrationEntry(user_id=current_user.id, fluid_type=fluid_type, amount_ml=amount_ml, caloric_val=caloric_val, timestamp=timestamp)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('main.log_hydration', date=log_form.timestamp.data.date().isoformat()))
    
    start = datetime.combine(selected_date, time.min, tzinfo=timezone.utc)
    end = datetime.combine(selected_date, time.max, tzinfo=timezone.utc)

    hydration_logs = current_user.get_hydration_entries(start_date=start, end_date=end)
    return render_template('log_hydration.html', form=log_form, hydration_logs=hydration_logs, selected_date=selected_date.isoformat())

@main.route('/log-medication', methods=['GET', 'POST'])
@login_required
def log_medication():
    log_form = MedicationLogForm()
    if log_form.validate_on_submit():
        med_name = log_form.med_name.data
        amount_mg = log_form.amount_mg.data
        frequency = log_form.frequency.data
        comment = log_form.comment.data
        log = MedicationEntry(user_id=current_user.id, med_name=med_name, amount_mg=amount_mg, frequency=frequency, comment=comment)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('main.log_medication'))

    medication_logs = current_user.get_medication_entries()
    return render_template('log_meds.html', form=log_form, medication_logs=medication_logs)

@main.route('/log-exercise', methods=['GET', 'POST'])
@login_required
def log_exercise():
    log_form = ExerciseLogForm()
    date_str = request.args.get('date') or date.today().isoformat()
    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        selected_date = datetime.fromisoformat(date_str).date()
    
    if request.method == 'GET':
        log_form.timestamp.data = datetime.combine(selected_date, datetime.now().time())
    
    if log_form.validate_on_submit():
        timestamp = log_form.timestamp.data.replace(tzinfo=timezone.utc)
        exercise_name = log_form.exercise_name.data
        minutes = log_form.minutes.data
        calories_burned = log_form.calories_burned.data
        log = ExerciseEntry(user_id=current_user.id, exercise_name=exercise_name, minutes=minutes, calories_burned=calories_burned, timestamp=timestamp)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('main.log_exercise', date=log_form.timestamp.data.date().isoformat()))
    
    start = datetime.combine(selected_date, time.min, tzinfo=timezone.utc)
    end = datetime.combine(selected_date, time.max, tzinfo=timezone.utc)

    exercise_logs = current_user.get_exercise_entries(start_date=start, end_date=end)
    return render_template('log_exercise.html', form=log_form, exercise_logs=exercise_logs, selected_date=selected_date.isoformat())

@main.route('/log-bowel', methods=['GET', 'POST'])
@login_required
def log_bowel():
    log_form = BowelLogForm()
    date_str = request.args.get('date') or date.today().isoformat()
    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        selected_date = datetime.fromisoformat(date_str).date()
    
    if request.method == 'GET':
        log_form.timestamp.data = datetime.combine(selected_date, datetime.now().time())
    
    if log_form.validate_on_submit():
        timestamp = log_form.timestamp.data.replace(tzinfo=timezone.utc)
        stool_type = log_form.stool_type.data
        stool_color = log_form.stool_color.data
        stool_description = log_form.stool_description.data
        log = BowelMovementEntry(user_id=current_user.id, stool_type=stool_type, stool_color=stool_color, stool_description=stool_description, timestamp=timestamp)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('main.log_bowel', date=log_form.timestamp.data.date().isoformat()))
    
    start = datetime.combine(selected_date, time.min, tzinfo=timezone.utc)
    end = datetime.combine(selected_date, time.max, tzinfo=timezone.utc)

    bowel_logs = current_user.get_bowel_movement_entries(start_date=start, end_date=end)
    return render_template('log_bowel.html', form=log_form, bowel_logs=bowel_logs, selected_date=selected_date.isoformat())

@main.route('/log-weight', methods=['GET', 'POST'])
@login_required
def log_weight():
    log_form = WeightLogForm()
    if log_form.validate_on_submit():
        weight_lbs = log_form.weight_lbs.data
        log = WeightEntry(user_id=current_user.id, weight_lbs=weight_lbs)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('main.log_weight'))

    weight_logs = current_user.get_weight_entries()
    return render_template('log_weight.html', form=log_form, weight_logs=weight_logs)

@main.route('/log-urine', methods=['GET', 'POST'])
@login_required
def log_urine():
    log_form = UrineLogForm()
    date_str = request.args.get('date') or date.today().isoformat()
    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        selected_date = datetime.fromisoformat(date_str).date()
    
    if request.method == 'GET':
        log_form.timestamp.data = datetime.combine(selected_date, datetime.now().time())
    
    if log_form.validate_on_submit():
        timestamp = log_form.timestamp.data.replace(tzinfo=timezone.utc)
        urine_color = log_form.urine_color.data
        urine_comment = log_form.urine_comment.data
        log = UrineEntry(user_id=current_user.id, urine_color=urine_color, urine_comment=urine_comment, timestamp=timestamp)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('main.log_urine', date=log_form.timestamp.data.date().isoformat()))
    
    start = datetime.combine(selected_date, time.min, tzinfo=timezone.utc)
    end = datetime.combine(selected_date, time.max, tzinfo=timezone.utc)
    
    urine_logs = current_user.get_urine_entries(start_date=start, end_date=end)
    return render_template('log_urine.html', form=log_form, urine_logs=urine_logs, selected_date=selected_date.isoformat())

@main.route('/hide-module/<module_name>', methods=['POST'])
@login_required
def hide_module(module_name):
    already_hidden = HiddenModule.query.filter_by(user_id=current_user.id, module_name=module_name).first()
    if not already_hidden:
        hidden = HiddenModule(user_id=current_user.id, module_name=module_name)
        db.session.add(hidden)
        db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/hide-and-delete-module/<module_name>', methods=['POST'])
@login_required
def hide_and_delete_module(module_name):
    already_hidden = HiddenModule.query.filter_by(user_id=current_user.id, module_name=module_name).first()
    if not already_hidden:
        hidden = HiddenModule(user_id=current_user.id, module_name=module_name)
        db.session.add(hidden)
        db.session.commit()

    # Delete all entries for this module
    if module_name == "food":
        entries = FoodEntry.query.filter_by(user_id=current_user.id).all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()
    elif module_name == "hydration":
        entries = HydrationEntry.query.filter_by(user_id=current_user.id).all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()
    elif module_name == "weight":
        entries = WeightEntry.query.filter_by(user_id=current_user.id).all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()
    elif module_name == "exercise":
        entries = ExerciseEntry.query.filter_by(user_id=current_user.id).all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()
    elif module_name == "bowel":
        entries = BowelMovementEntry.query.filter_by(user_id=current_user.id).all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()
    elif module_name == "sleep":
        entries = SleepEntry.query.filter_by(user_id=current_user.id).all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()
    elif module_name == "urine":
        entries = UrineEntry.query.filter_by(user_id=current_user.id).all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()
    elif module_name == "medication":
        entries = MedicationEntry.query.filter_by(user_id=current_user.id).all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()

    return redirect(url_for('main.dashboard'))


@main.route('/add-module/<module_name>', methods=['POST'])
@login_required
def add_module(module_name):
    hidden = HiddenModule.query.filter_by(user_id=current_user.id, module_name=module_name).first()
    if hidden:
        db.session.delete(hidden)
        db.session.commit()
    return redirect(url_for('main.dashboard'))
