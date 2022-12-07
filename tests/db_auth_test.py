from src.database.session import SessionLocal
from src.services import auth_operations
from src.models import User


session = SessionLocal()


TEST_USER = User(name='test', email='test', password='test')
TEST_USER.id = -2


def test_blank_get_user_by_id():
    user = auth_operations.get_user_by_id(-1)
    assert user is None


def test_blank_get_user_by_email():
    user = auth_operations.get_user_by_email('')
    assert user is None


def test_get_user_by_id():
    session.add(TEST_USER)
    session.commit()

    user = auth_operations.get_user_by_id(TEST_USER.id)

    session.query(User).filter(User.id == TEST_USER.id).delete()
    session.commit()

    assert user is not None


def test_get_user_by_email():
    session.add(TEST_USER)
    session.commit()

    user = auth_operations.get_user_by_email(TEST_USER.email)

    session.query(User).filter(User.id == TEST_USER.id).delete()
    session.commit()

    assert user is not None


def test_post_create_new_user():
    auth_operations.post_create_new_user(TEST_USER)

    user = session.query(User).filter(User.id == TEST_USER.id).first()

    session.query(User).filter(User.id == TEST_USER.id).delete()
    session.commit()

    assert user is not None
