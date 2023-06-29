from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_moment import Moment
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
photos = UploadSet('photos', IMAGES)
moment = Moment()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)
    moment.init_app(app)
    configure_uploads(app, photos)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models