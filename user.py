from flask_login import LoginManager
from database import User

login_manager = LoginManager()

def init_login_manager(app, db):
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, user_id)