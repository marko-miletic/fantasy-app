from sqlalchemy import and_
from src.database.session import SessionLocal
from src.models import League, User, UserLeague
from src.crud import league_operations


session = SessionLocal()


def test_add_user_to_league():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    test_league = League(name='test', owner_id=test_user.id)
    test_league.id = -1

    session.add(test_user)
    session.commit()

    session.add(test_league)
    session.commit()

    league_operations.post_add_user_to_league(user_id=test_user.id, league_id=test_league.id)

    league_player = session.query(UserLeague).filter(UserLeague.league_id == test_league.id).first()

    session.query(UserLeague).filter(UserLeague.league_id == test_league.id).delete()
    session.query(League).filter(League.id == test_league.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert league_player is not None and league_player.user_id == test_user.id


def test_approve_new_league_player():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    test_league = League(name='test', owner_id=test_user.id)
    test_league.id = -1

    test_user_league = UserLeague(user_id=test_user.id, league_id=test_league.id)
    test_user_league.id = -1

    session.add(test_user)
    session.commit()

    session.add(test_league)
    session.commit()

    session.add(test_user_league)
    session.commit()
    
    league_operations.update_approve_new_league_player(league_id=test_league.id, user_id=test_user.id)

    league_player = session.query(UserLeague)\
        .filter(and_(UserLeague.user_id == test_user.id, UserLeague.league_id == test_league.id)).first()

    session.query(UserLeague).filter(UserLeague.league_id == test_league.id).delete()
    session.query(League).filter(League.id == test_league.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert league_player is not None and league_player.approved_access is True


def test_create_new_league():
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


def test_get_league_by_id():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    test_league = League(name='test', owner_id=test_user.id)
    test_league.id = -1

    session.add(test_user)
    session.commit()

    session.add(test_league)
    session.commit()

    league = league_operations.get_league_by_id(league_id=test_league.id)

    session.query(League).filter(League.id == test_league.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert league is not None and league.get('id', None) == test_league.id 


def test_get_league_by_owner():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    test_league = League(name='test', owner_id=test_user.id)
    test_league.id = -1

    session.add(test_user)
    session.commit()

    session.add(test_league)
    session.commit()

    league = league_operations.get_league_by_owner(owner_id=test_user.id)

    session.query(League).filter(League.id == test_league.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert league is not None and league[0].get('owner_id', None) == test_user.id 


def test_get_league_rankings_by_league_id():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    test_league = League(name='test', owner_id=test_user.id)
    test_league.id = -1

    test_user_league = UserLeague(user_id=test_user.id, league_id=test_league.id)
    test_user_league.id = -1

    session.add(test_user)
    session.commit()

    session.add(test_league)
    session.commit()

    session.add(test_user_league)
    session.commit()

    league_rankings = league_operations.get_league_rankings_by_league_id(league_id=test_league.id)
    print(league_rankings)

    session.query(UserLeague).filter(UserLeague.league_id == test_league.id).delete()
    session.query(League).filter(League.id == test_league.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert league_rankings is not None and \
           len(league_rankings) == 1 and \
           league_rankings[0].get('points', -1) == 0
    