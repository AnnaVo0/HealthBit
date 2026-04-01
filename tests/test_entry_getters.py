from app import app, db
import pytest
from database import User, FoodEntry, WaterEntry, BowelMovementEntry, ExerciseEntry, WeightEntry
from datetime import datetime, timedelta

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

def test_user_get_food_entries(client):
    user = client.query(User).filter_by(username="testuser").first()
    now = datetime.now()
    
    client.add(FoodEntry(user_id=user.id, food_name="Apple", calories=5, timestamp=now - timedelta(days=5)))
    client.add(FoodEntry(user_id=user.id, food_name="Banana", calories=10, timestamp=now))
    client.add(FoodEntry(user_id=user.id, food_name="Burger", calories=100, timestamp=now + timedelta(days=5)))
    client.commit()
    
    start_only = user.get_food_entries(start_date=now - timedelta(days=1))
    assert len(start_only) == 2
    assert start_only[0].food_name == "Banana"
    assert start_only[1].food_name == "Burger"
    
    end_only = user.get_food_entries(end_date=now + timedelta(days=1))
    assert len(end_only) == 2
    assert end_only[0].food_name == "Apple"
    assert end_only[1].food_name == "Banana"
    
    both = user.get_food_entries(start_date=now - timedelta(days=1), end_date=now + timedelta(days=1))
    assert len(both) == 1
    assert both[0].food_name == "Banana"

def test_user_get_water_entries(client):
    user = client.query(User).filter_by(username="testuser").first()
    now = datetime.now()
    
    client.add(WaterEntry(user_id=user.id, amount_ml=100, timestamp=now - timedelta(days=5)))
    client.add(WaterEntry(user_id=user.id, amount_ml=200, timestamp=now))
    client.add(WaterEntry(user_id=user.id, amount_ml=300, timestamp=now + timedelta(days=5)))
    client.commit()
    
    start_only = user.get_water_entries(start_date=now - timedelta(days=1))
    assert len(start_only) == 2
    assert start_only[0].amount_ml == 200
    assert start_only[1].amount_ml == 300
    
    end_only = user.get_water_entries(end_date=now + timedelta(days=1))
    assert len(end_only) == 2
    assert end_only[0].amount_ml == 100
    assert end_only[1].amount_ml == 200
    
    both = user.get_water_entries(start_date=now - timedelta(days=1), end_date=now + timedelta(days=1))
    assert len(both) == 1
    assert both[0].amount_ml == 200

def test_user_get_weight_entries(client):
    user = client.query(User).filter_by(username="testuser").first()
    now = datetime.now()
    
    client.add(WeightEntry(user_id=user.id, weight_lbs=250, timestamp=now - timedelta(days=5)))
    client.add(WeightEntry(user_id=user.id, weight_lbs=150, timestamp=now))
    client.add(WeightEntry(user_id=user.id, weight_lbs=200, timestamp=now + timedelta(days=5)))
    client.commit()
    
    start_only = user.get_weight_entries(start_date=now - timedelta(days=1))
    assert len(start_only) == 2
    assert start_only[0].weight_lbs == 150
    assert start_only[1].weight_lbs == 200
    
    end_only = user.get_weight_entries(end_date=now + timedelta(days=1))
    assert len(end_only) == 2
    assert end_only[0].weight_lbs == 250
    assert end_only[1].weight_lbs == 150
    
    both = user.get_weight_entries(start_date=now - timedelta(days=1), end_date=now + timedelta(days=1))
    assert len(both) == 1
    assert both[0].weight_lbs == 150

def test_user_get_exercise_entries(client):
    user = client.query(User).filter_by(username="testuser").first()
    now = datetime.now()
    
    client.add(ExerciseEntry(user_id=user.id, exercise_name="Running", minutes=30, calories_burned=300, timestamp=now - timedelta(days=5)))
    client.add(ExerciseEntry(user_id=user.id, exercise_name="Walking", minutes=60, calories_burned=200, timestamp=now))
    client.add(ExerciseEntry(user_id=user.id, exercise_name="Weight Lifting", minutes=45, calories_burned=400, timestamp=now + timedelta(days=5)))
    client.commit()
    
    start_only = user.get_exercise_entries(start_date=now - timedelta(days=1))
    assert len(start_only) == 2
    assert start_only[0].exercise_name == "Walking"
    assert start_only[1].exercise_name == "Weight Lifting"
    
    end_only = user.get_exercise_entries(end_date=now + timedelta(days=1))
    assert len(end_only) == 2
    assert end_only[0].exercise_name == "Running"
    assert end_only[1].exercise_name == "Walking"
    
    both = user.get_exercise_entries(start_date=now - timedelta(days=1), end_date=now + timedelta(days=1))
    assert len(both) == 1
    assert both[0].exercise_name == "Walking"

def test_user_get_bowel_movement_entries(client):
    user = client.query(User).filter_by(username="testuser").first()
    now = datetime.now()
    
    client.add(BowelMovementEntry(user_id=user.id, stool_type="1", stool_description="Hard", stool_color="Brown", timestamp=now - timedelta(days=5)))
    client.add(BowelMovementEntry(user_id=user.id, stool_type="3", stool_description="Solid", stool_color="Brown", timestamp=now))
    client.add(BowelMovementEntry(user_id=user.id, stool_type="4", stool_description="Smooth", stool_color="Brown", timestamp=now + timedelta(days=5)))
    client.commit()
    
    start_only = user.get_bowel_movement_entries(start_date=now - timedelta(days=1))
    assert len(start_only) == 2
    assert start_only[0].stool_type == "3"
    assert start_only[1].stool_type == "4"
    
    end_only = user.get_bowel_movement_entries(end_date=now + timedelta(days=1))
    assert len(end_only) == 2
    assert end_only[0].stool_type == "1"
    assert end_only[1].stool_type == "3"
    
    both = user.get_bowel_movement_entries(start_date=now - timedelta(days=1), end_date=now + timedelta(days=1))
    assert len(both) == 1
    assert both[0].stool_type == "3"