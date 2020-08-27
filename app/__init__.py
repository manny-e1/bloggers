from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from flask_migrate import Migrate
from flask_compress import Compress
from app.config import Config

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500


# bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
mail = Mail()
compress = Compress()
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    # bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    compress.init_app(app)
    
    from app.auth import users
    from app.posts import posts
    from app.main import main
    from app.api import api
    # from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')
    # app.register_blueprint(errors)

    return app