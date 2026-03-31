from app import app, db
from flask_login import LoginManager

from database import User
    
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)