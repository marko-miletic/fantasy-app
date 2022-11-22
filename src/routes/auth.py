from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request
)

from flask_login import (
    login_user,
    login_required,
    logout_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from src.models.user import User
from src.services.auth_operations import (
    post_create_new_user,
    get_user_by_email
)

from src.path_structure import TEMPLATES_DIRECTORY_PATH


auth = Blueprint('auth', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)

@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = get_user_by_email(email)

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('index.profile'))


@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = get_user_by_email(email)
    print(user)
    if user:
        return redirect(url_for('auth.signup'))

    new_user_object = User(
        name=name,
        email=email,
        password=generate_password_hash(password, method='sha256')
    )
    # add the new user to the database
    post_create_new_user(new_user_object)

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.main'))
