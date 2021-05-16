from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from  sqlalchemy.exc import OperationalError
import os, secrets, sys
from hashlib import sha256

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_secret(logger):
    secret = secrets.token_hex(32)
    logger.warn("No secret provided in the SECRET_KEY environment variable. Using %s for this session", secret)
    return secret

# checkes if the DB is seeded and seeds if it's not
def seed_db(db, logger):
    logger.warn("Database is being initialized")
    try:
        with db.engine.connect() as con:
            salt = secrets.token_hex(16)
            passwordHash = sha256('{}:{}'.format(salt, "admin").encode('utf-8')).hexdigest()
            con.execute("INSERT into users (id, username, salt, password, data) VALUES (0, 'admin', '{}', '{}', '')".format(salt, passwordHash))
    except OperationalError as e:
        logger.warn("Failed to add admin user: %2", e.detail)
        return False
    else:
        return True

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or create_secret(app.logger)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////var/pi-env/db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.app_context().push()
    from .models import User
    weGood = True
    try:
        userCount = db.session.query(User).count()
        if userCount == 0:
            weGood = seed_db(db, app.logger)
    except OperationalError:
        # No DB setup. Create it:
        db.create_all()
        weGood = seed_db(db, app.logger)
    
    if not weGood:
        app.logger.error("Exiting because of DB issue")
        sys.exit(3)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app