from flask import Flask

from src.routes import *


def build_app():
    app = Flask(__name__)
    
    app.register_blueprint(index.index, url_prefix='/')

    from src.core.cache import cache  
    cache.init_app(app=app)

    return app
