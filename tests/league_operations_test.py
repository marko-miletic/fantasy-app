from src.database.session import SessionLocal
from src.models import League, User, UserLeague
from src.crud import league_operations


session = SessionLocal()


def test_add_player_to_lineup():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    test_league_name = 'test'

    session.add(test_user)
    session.commit()

    league_operations.post_create_new_league(league_name=test_league_name, owner_id=test_user.id)

    league = session.query(League).filter(League.owner_id == test_user.id).first()

    session.query(League).filter(League.owner_id == test_user.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert league is not None and league.name == test_league_name
