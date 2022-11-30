from src.models.user import User
from src.database.session import SessionLocal
from src.core.config import admin_default_account


session = SessionLocal()


def test_database_admin_user():
    admin = session.query(User).filter(User.name == admin_default_account.USER).scalar()
    assert admin is not None
