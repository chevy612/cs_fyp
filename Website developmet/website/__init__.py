from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "key_answer_db"

def create_app():
    app = Flask(__name__)

    # MySQL setup
    app.config["SECRET_KEY"] = "chevy612"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:Cc67440640@localhost/{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    #migrate = Migrate(app,db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Search
    with app.app_context():
        create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "views.home"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        db.create_all()  # Create new tables if they do not exist
        print("Created Database!")


