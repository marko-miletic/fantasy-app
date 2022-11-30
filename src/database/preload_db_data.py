import os

from src.database.session import SessionLocal
from src.core.config import admin_default_account
from src.path_structure import ASSETS_DIRECTORY_PATH
from src.models.user import User

from werkzeug.security import generate_password_hash


session = SessionLocal()


DATA_DIRECTORY_PATH = os.path.join(ASSETS_DIRECTORY_PATH, 'data')


def add_default_admin_user() -> None:
    test_sample_query = session.query(User).filter(User.name == admin_default_account.USER).scalar()
    if test_sample_query:
        return None

    default_admin_user = User(
        name=admin_default_account.USER,
        email=admin_default_account.MAIL,
        password=generate_password_hash(admin_default_account.PASSWORD, method='sha256'),
        role=2
    )

    session.add(default_admin_user)
    session.commit()

    return None


def fill_db_data() -> None:
    
    add_default_admin_user()

    return None
