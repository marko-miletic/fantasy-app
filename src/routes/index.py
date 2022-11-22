from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)


from src.path_structure import TEMPLATES_DIRECTORY_PATH


index = Blueprint('index', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@index.route('/')
def main():
    return render_template('index.html')


@index.route('/profile')
@login_required
def profile():
    return render_template(
        'profile.html',
        name=current_user.name
    )
