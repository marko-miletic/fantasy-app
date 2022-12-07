from src.database.session import SessionLocal
from src.models import Match, GoalsScored, Points, User


session = SessionLocal()


def test_post_create_new_match():
    test_match = Match(date='1980-1-1', home_team_id=0, away_team_id=1)
    test_match.id = -1

    session.add(test_match)
    session.commit()

    match = session.query(Match).filter(Match.id == test_match.id).first()

    session.query(Match).filter(Match.id == test_match.id).delete()
    session.commit()

    assert match is not None


def test_post_goals_scored():
    test_match = Match(date='1980-1-1', home_team_id=0, away_team_id=1)
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
    test_match = Match(date='1980-1-1', home_team_id=0, away_team_id=1)
    test_match.id = -1
    test_user = User(name='test', email='test', password='test')
    test_user.id = -2
    test_points = Points(number_of_points=-1, match_id=-1, user_id=-2)

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
