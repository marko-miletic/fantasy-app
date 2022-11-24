from flask import Flask

from src.routes import *
from src.core.authentication import login_manager
from src.services.auth_operations import get_user_by_id

from os import getenv
from dotenv import load_dotenv


def build_app():
    app = Flask(__name__)

    load_dotenv()
    app.config['SECRET_KEY'] = getenv('FLASK_AUTH_SECRET_KEY')

    app.register_blueprint(index.index, url_prefix='/')
    app.register_blueprint(auth.auth, url_prefix='/auth')
    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

    from src.core.cache import cache
    cache.init_app(app=app)

    return app
