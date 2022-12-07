from src.database.session import SessionLocal
from src.models import Match, GoalsScored, Points, User


session = SessionLocal()


TEST_MATCH = Match(date='1980-1-1', home_team_id=0, away_team_id=1)
TEST_MATCH.id = -1

TEST_GOALS_SCORED = GoalsScored(number_of_goals=-1, match_id=-1, player_id=0)
TEST_GOALS_SCORED.id = -1

TEST_USER = User(name='test', email='test', password='test')
TEST_USER.id = -2
TEST_POINTS = Points(number_of_points=-1, match_id=-1, user_id=-2)


def test_post_create_new_match():
    session.add(TEST_MATCH)
    session.commit()

    match = session.query(Match).filter(Match.id == TEST_MATCH.id).first()

    session.query(Match).filter(Match.id == TEST_MATCH.id).delete()
    session.commit()

    assert match is not None


def test_post_goals_scored():
    session.add(TEST_MATCH)
    session.commit()
    session.add(TEST_GOALS_SCORED)
    session.commit()

    goals_by_player = session.query(GoalsScored).filter(GoalsScored.id == TEST_GOALS_SCORED.id).first()

    session.query(GoalsScored).filter(GoalsScored.id == TEST_GOALS_SCORED.id).delete()
    session.query(Match).filter(Match.id == TEST_MATCH.id).delete()
    session.commit()

    assert goals_by_player is not None


def test_post_points():
    session.add(TEST_MATCH)
    session.commit()
    session.add(TEST_USER)
    session.commit()
    session.add(TEST_POINTS)
    session.commit()

    points_by_user_per_match = session.query(Points).filter(Points.id == TEST_POINTS.id).first()

    session.query(Points).filter(Points.id == TEST_POINTS.id).delete()
    session.query(User).filter(User.id == TEST_USER.id).delete()
    session.query(Match).filter(Match.id == TEST_MATCH.id).delete()
    session.commit()

    assert points_by_user_per_match is not None
