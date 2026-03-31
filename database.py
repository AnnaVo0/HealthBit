from flask_login import UserMixin
from sqlalchemy.orm import relationship
from app import db
from config import usernameMaxLen, pwdMaxLen

class User(db.Model, UserMixin): 
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(usernameMaxLen), nullable=False, unique=True)
    password = db.Column(db.String(pwdMaxLen), nullable=False)
    
    entries = relationship("Entry", backref="user", cascade="all, delete-orphan")

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
    food_name = db.Column(db.String(100))
    calories = db.Column(db.Integer)

    __mapper_args__ = {"polymorphic_identity": "food"}

class WaterEntry(Entry):
    __tablename__ = "water_entries"
    id = db.Column(db.Integer, db.ForeignKey("entries.id"), primary_key=True)
    amount_ml = db.Column(db.Integer)

    __mapper_args__ = {"polymorphic_identity": "water"}
    
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