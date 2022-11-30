from src.database.session import SessionLocal
from src.models.user import User


session = SessionLocal()


def get_user_by_id(user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    return user


def get_user_by_email(email: str) -> User:
    user = session.query(User).filter_by(email=email).first()
    return user


def post_create_new_user(new_user_object: User) -> None:
    session.add(new_user_object)
    session.commit()

