from src.database.session import SessionLocal
from src.models import Match, GoalsScored, Points, User
from src.crud import match_operations


session = SessionLocal()


def test_post_create_new_match():
    test_match = Match(date='1980-1-1', match_round=-1, home_team_id=0, away_team_id=1)
    test_match.id = -1

    session.add(test_match)
    session.commit()

    match = session.query(Match).filter(Match.id == test_match.id).first()

    session.query(Match).filter(Match.id == test_match.id).delete()
    session.commit()

    assert match is not None


def test_get_matches_by_status():
    test_match = Match(date='1980-1-1', match_round=-1, home_team_id=0, away_team_id=1)
    test_match.id = -1
    test_match.status = 'active'

    session.add(test_match)
    session.commit()

    status_matches = match_operations.get_matches_by_status(test_match.status)

    session.query(Match).filter(Match.round == test_match.round).delete()
    session.commit()

    correct_status_count = 0
    for match in status_matches:
        if not match.get('confirmed', True):
            correct_status_count += 1

    assert len(status_matches) == correct_status_count and len(status_matches) > 0


def test_get_matches_by_round():
    test_match = Match(date='1980-1-1', match_round=-1, home_team_id=0, away_team_id=1)
    test_match.id = -1

    session.add(test_match)
    session.commit()

    round_matches = match_operations.get_matches_by_round(match_round=test_match.round)

    session.query(Match).filter(Match.round == test_match.round).delete()
    session.commit()

    assert len(round_matches) == 1 and round_matches[0].get('round', None) == test_match.round


def test_get_matches_by_id():
    test_match = Match(date='1980-1-1', match_round=-1, home_team_id=0, away_team_id=1)
    test_match.id = -1

    session.add(test_match)
    session.commit()

    id_match = match_operations.get_match_by_id(match_id=test_match.id)

    session.query(Match).filter(Match.id == test_match.id).delete()
    session.commit()

    assert id_match is not None and id_match.get('id', None) == test_match.id


def test_post_goals_scored():
    test_match = Match(date='1980-1-1', match_round=-1,  home_team_id=0, away_team_id=1)
    test_match.id = -1

    test_goals_scored = GoalsScored(number_of_goals=-1, match_id=-1, player_id=0)
    test_goals_scored.id = -1

    session.add(test_match)
    session.commit()
    session.add(test_goals_scored)
    session.commit()

    goals_by_player = session.query(GoalsScored).filter(GoalsScored.id == test_goals_scored.id).first()

    session.query(GoalsScored).filter(GoalsScored.id == test_goals_scored.id).delete()
    session.query(Match).filter(Match.id == test_match.id).delete()
    session.commit()

    assert goals_by_player is not None


def test_post_points():
    test_match = Match(date='1980-1-1', match_round=-1, home_team_id=0, away_team_id=1)
    test_match.id = -1
    test_user = User(name='test', email='test', password='test')
    test_user.id = -2
    test_points = Points(number_of_points=-1, match_id=-1, player_id=0)

    session.add(test_match)
    session.commit()
    session.add(test_user)
    session.commit()
    session.add(test_points)
    session.commit()

    points_by_user_per_match = session.query(Points).filter(Points.id == test_points.id).first()

    session.query(Points).filter(Points.id == test_points.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.query(Match).filter(Match.id == test_match.id).delete()
    session.commit()

    assert points_by_user_per_match is not None
