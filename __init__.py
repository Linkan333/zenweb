from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'signin'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from models import User  # Import User here to avoid circular imports
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from models import User  # Import User model inside this function
    return User.query.get(int(user_id))  # Query user by ID
