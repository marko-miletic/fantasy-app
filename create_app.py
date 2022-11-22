from flask import Flask

from src.routes import *
from src.core.authentication import login_manager
from src.services.auth_operations import get_user_by_id

def build_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'bla-bla-bla'

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
