from flask import Flask

from src import routes

from src.core.authentication import login_manager
from src.core.config import auth_app_settings

from src.services.auth_operations import get_user_by_id

from src.database.preload_db_data import fill_db_data


def build_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = auth_app_settings.AUTH_SECRET_KEY

    app.register_blueprint(routes.index.index, url_prefix='/')
    app.register_blueprint(routes.auth.auth, url_prefix='/auth')
    app.register_blueprint(routes.lineup.lineup, url_prefix='/lineup')
    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

    from src.core.cache import cache
    cache.init_app(app=app)

    fill_db_data()

    return app
