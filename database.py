from flask_login import UserMixin
from sqlalchemy.orm import relationship
from config import usernameMaxLen, pwdMaxLen
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin): 
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(usernameMaxLen), nullable=False, unique=True)
    password = db.Column(db.String(pwdMaxLen), nullable=False)
    
    entries = relationship("Entry", backref="user", cascade="all, delete-orphan")
    
    def get_food_entries(self, start_date=None, end_date=None):
        query = FoodEntry.query.filter_by(user_id=self.id)
        if start_date:
            query = query.filter(FoodEntry.timestamp >= start_date)
        if end_date:
            query = query.filter(FoodEntry.timestamp <= end_date)
        return query.all()

    def get_hydration_entries(self, start_date=None, end_date=None):
        query = HydrationEntry.query.filter_by(user_id=self.id)
        if start_date:
            query = query.filter(HydrationEntry.timestamp >= start_date)
        if end_date:
            query = query.filter(HydrationEntry.timestamp <= end_date)
        return query.all()
        
    def get_weight_entries(self, start_date=None, end_date=None):
        query = WeightEntry.query.filter_by(user_id=self.id)
        if start_date:
            query = query.filter(WeightEntry.timestamp >= start_date)
        if end_date:
            query = query.filter(WeightEntry.timestamp <= end_date)
        return query.all()

    def get_exercise_entries(self, start_date=None, end_date=None):
        query = ExerciseEntry.query.filter_by(user_id=self.id)
        if start_date:
            query = query.filter(ExerciseEntry.timestamp >= start_date)
        if end_date:
            query = query.filter(ExerciseEntry.timestamp <= end_date)
        return query.all()

    def get_bowel_movement_entries(self, start_date=None, end_date=None):
        query = BowelMovementEntry.query.filter_by(user_id=self.id)
        if start_date:
            query = query.filter(BowelMovementEntry.timestamp >= start_date)
        if end_date:
            query = query.filter(BowelMovementEntry.timestamp <= end_date)
        return query.all()

    def get_sleep_entries(self, start_date=None, end_date=None):
        query = SleepEntry.query.filter_by(user_id=self.id)
        if start_date:
            query = query.filter(SleepEntry.timestamp >= start_date)
        if end_date:
            query = query.filter(SleepEntry.timestamp <= end_date)
        return query.all()

    def get_urine_entries(self, start_date=None, end_date=None):
        pass

    def get_medication_entries(self, start_date=None, end_date=None):
        query = MedicationEntry.query.filter_by(user_id=self.id)
        if start_date:
            query = query.filter(MedicationEntry.timestamp >= start_date)
        if end_date:
            query = query.filter(MedicationEntry.timestamp <= end_date)
        return query.all()
    
class Entry(db.Model):
    __tablename__ = "entries"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    entry_type = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    __mapper_args__ = {
        "polymorphic_identity": "entry",
        "polymorphic_on": entry_type,
    }

class FoodEntry(Entry):
    __tablename__ = "food_entries"
    id = db.Column(db.Integer, db.ForeignKey("entries.id"), primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)

    # Flask will error out without a proper __init__() declared here
    # For child entries that inherit from Entry, only user_id needs to be set in __init__() + any new child class-specific attributes
    def __init__(self, user_id, food_name, calories):
        self.user_id = user_id
        self.food_name = food_name
        self.calories = calories

    __mapper_args__ = {"polymorphic_identity": "food"}

class HydrationEntry(Entry):
    __tablename__ = "hydration_entries"
    id = db.Column(db.Integer, db.ForeignKey("entries.id"), primary_key=True)
    fluid_type = db.Column(db.String(100), nullable=False)
    amount_ml = db.Column(db.Integer, nullable=False)
    caloric_val = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, fluid_type, amount_ml, caloric_val):
        self.user_id = user_id
        self.fluid_type = fluid_type
        self.amount_ml = amount_ml
        self.caloric_val = caloric_val

    __mapper_args__ = {"polymorphic_identity": "hydration"}
    
class WeightEntry(Entry):
    __tablename__ = "weight_entries"
    id = db.Column(db.Integer, db.ForeignKey("entries.id"), primary_key=True)
    weight_lbs = db.Column(db.Integer)

    __mapper_args__ = {"polymorphic_identity": "weight"}

class ExerciseEntry(Entry):
    __tablename__ = "exercise_entries"
    id = db.Column(db.Integer, db.ForeignKey("entries.id"), primary_key=True)
    exercise_name = db.Column(db.String(100))
    minutes = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)

    __mapper_args__ = {"polymorphic_identity": "exercise"}

class BowelMovementEntry(Entry):
    __tablename__ = "bowel_movement_entries"
    id = db.Column(db.Integer, db.ForeignKey("entries.id"), primary_key=True)
    stool_type = db.Column(db.String(100))
    stool_description = db.Column(db.String(100))
    stool_color = db.Column(db.String(100))

    __mapper_args__ = {"polymorphic_identity": "bowel_movement"}


class UrineEntry(Entry):
    pass

class SleepEntry(Entry):
    __tablename__ = "sleep_entries"
    id = db.Column(db.Integer, db.ForeignKey("entries.id"), primary_key=True)
    sleep_duration = db.Column(db.Integer, nullable=False)
    sleep_quality = db.Column(db.String(100), nullable=False)
    sleep_comment = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, sleep_duration, sleep_quality, sleep_comment):
        self.user_id = user_id
        self.sleep_duration = sleep_duration
        self.sleep_quality = sleep_quality
        self.sleep_comment = sleep_comment

    __mapper_args__ = {"polymorphic_identity": "sleep"}

class MedicationEntry(Entry):
    __tablename__ = "medication_entries"
    id = db.Column(db.Integer, db.ForeignKey("entries.id"), primary_key=True)
    med_name = db.Column(db.String(100), nullable=False)
    amount_mg = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(100), nullable=True)

    def __init__(self, user_id, med_name, amount_mg, frequency, comment):
        self.user_id = user_id
        self.med_name = med_name
        self.amount_mg = amount_mg
        self.frequency = frequency
        self.comment = comment

    __mapper_args__ = {"polymorphic_identity": "medication"}