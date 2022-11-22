from flask import Blueprint
from flask import (
    make_response
)


from src.path_structure import TEMPLATES_DIRECTORY_PATH


index = Blueprint('index', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@index.route('/', methods=['GET'])
@index.route('/home', methods=['GET'])
@index.route('/index', methods=['GET'])
def index_page():
    return make_response({'status': 200})
