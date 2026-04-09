from app import app
from database import db
import pytest
from database import User, FoodEntry, HydrationEntry, BowelMovementEntry, ExerciseEntry, WeightEntry

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        test_user = User(username="testuser", password="testpassword")
        db.session.add(test_user)
        db.session.commit()
        
        yield db.session
        
        db.session.remove()
        db.drop_all()

@pytest.mark.parametrize("name, cals", [
    ("Apple", 5),
    ("Banana", 10),
    ("Pizza", 1000),
    ("Coca-Cola", 500)
])
def test_food_entry(client, name, cals):
    user = client.query(User).filter_by(username="testuser").first()
    
    entry = FoodEntry(user_id=user.id, food_name=name, calories=cals)
    client.add(entry)
    client.commit()
    
    result = client.query(FoodEntry).filter_by(food_name=name, calories=cals).first()
    assert result is not None
    assert result.food_name == name
    assert result.calories == cals
    
@pytest.mark.parametrize("ml", [
    (95),
    (105),
    (285),
    (500)
])
def test_fluid_entry(client, ml):
    user = client.query(User).filter_by(username="testuser").first()
    
    entry = HydrationEntry(user_id=user.id, fluid_type="Water", amount_ml=ml, caloric_val=0)
    client.add(entry)
    client.commit()
    
    result = client.query(HydrationEntry).filter_by(amount_ml=ml).first()
    assert result is not None
    assert result.amount_ml == ml
    
@pytest.mark.parametrize("lbs", [
    (95),
    (105),
    (285),
    (500)
])
def test_weight_entry(client, lbs):
    user = client.query(User).filter_by(username="testuser").first()
    
    entry = WeightEntry(user_id=user.id, weight_lbs=lbs)
    client.add(entry)
    client.commit()
    
    result = client.query(WeightEntry).filter_by(weight_lbs=lbs).first()
    assert result is not None
    assert result.weight_lbs == lbs
    
@pytest.mark.parametrize("name, mins, cals", [
    ("Running", 60, 100),
    ("Running", 20, 50),
    ("Walking", 65, 105),
    ("Weight Lifting", 10, 10)
])
def test_exercise_entry(client, name, mins, cals):
    user = client.query(User).filter_by(username="testuser").first()
    
    entry = ExerciseEntry(user_id=user.id, exercise_name=name, minutes=mins, calories_burned=cals)
    client.add(entry)
    client.commit()
    
    result = client.query(ExerciseEntry).filter_by(exercise_name=name, minutes=mins, calories_burned=cals).first()
    assert result is not None
    assert result.exercise_name == name
    assert result.minutes == mins
    assert result.calories_burned == cals
    
@pytest.mark.parametrize("typ, desc, color", [
    ("One", "Soft", "Brown"),
    ("One", "Solid", "Green"),
    ("Two", "Solid", "Light Brown"),
])
def test_bowel_movement_entry(client, typ, desc, color):
    user = client.query(User).filter_by(username="testuser").first()
    
    entry = BowelMovementEntry(user_id=user.id, stool_type=typ, stool_description=desc, stool_color=color)
    client.add(entry)
    client.commit()
    
    result = client.query(BowelMovementEntry).filter_by(stool_type=typ, stool_description=desc, stool_color=color).first()
    assert result is not None
    assert result.stool_type == typ
    assert result.stool_description == desc
    assert result.stool_color == color