from app import app, db
from flask_login import LoginManager, UserMixin

usernameMinLen = 4
usernameMaxLen = 20
pwdMinLen = 8
pwdMaxLen = 150

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(usernameMaxLen), nullable=False, unique=True)
    password = db.Column(db.String(pwdMaxLen), nullable=False)
    
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)