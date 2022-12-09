from src.database.session import SessionLocal
from src.models import User, SelectedPlayers, LineupLimits
from src.crud import auth_operations, lineup_operations


session = SessionLocal()


def test_add_player_to_lineup():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    auth_operations.post_create_new_user(test_user)
    lineup_operations.add_player_to_lineup(test_user.id, 0)

    test_lineup = session.query(SelectedPlayers).filter(SelectedPlayers.user_id == test_user.id).scalar()

    session.query(SelectedPlayers).filter(SelectedPlayers.user_id == test_user.id).delete()
    session.commit()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert test_lineup is not None


def test_get_lineup():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    auth_operations.post_create_new_user(test_user)
    lineup_operations.add_player_to_lineup(test_user.id, 0)

    test_lineup = lineup_operations.get_lineup(test_user.id)

    session.query(SelectedPlayers).filter(SelectedPlayers.user_id == test_user.id).delete()
    session.commit()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert len(test_lineup) == 1


def test_get_lineup_limits():
    full_lineup_limits = session.query(LineupLimits).filter(LineupLimits.lineup_status == 'full').scalar()
    active_lineup_limits = session.query(LineupLimits).filter(LineupLimits.lineup_status == 'active').scalar()

    assert full_lineup_limits is not None and active_lineup_limits is not None
