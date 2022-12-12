from src.database.session import SessionLocal
from src.models import User, UserPoints
from src.crud import points_operations


session = SessionLocal()


def test_post_user_point_for_given_round():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    points_operations.post_user_points_for_given_round(test_user.id, -1, -1)

    points_data = session.query(UserPoints).filter(UserPoints.user_id == test_user.id).first()

    session.query(UserPoints).filter(UserPoints.user_id == test_user.id).delete()
    session.commit()

    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert points_data is not None and points_data.points_count == -1


def test_get_points_per_user_per_round():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    test_user_points = UserPoints(user_id=test_user.id, round=-1, points_count=-1)

    session.add(test_user_points)
    session.commit()

    round_points_count = points_operations.get_points_per_user_per_round(user_id=test_user.id,
                                                                         round_number=test_user_points.round)

    test_user_points = int(test_user_points.points_count)

    session.query(UserPoints).filter(UserPoints.user_id == test_user.id).delete()
    session.commit()

    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert round_points_count is not None and round_points_count.get('points', None) == test_user_points


def test_get_points_per_user():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    test_user_points_1 = UserPoints(user_id=test_user.id, round=-1, points_count=-1)
    test_user_points_2 = UserPoints(user_id=test_user.id, round=-2, points_count=-2)

    session.add(test_user_points_1)
    session.add(test_user_points_2)
    session.commit()

    total_points_count = points_operations.get_points_per_user(user_id=test_user.id)

    test_user_points_1 = int(test_user_points_1.points_count)
    test_user_points_2 = int(test_user_points_2.points_count)

    session.query(UserPoints).filter(UserPoints.user_id == test_user.id).delete()
    session.commit()

    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert total_points_count is not None and \
           total_points_count.get('points', None) == test_user_points_1 + test_user_points_2
