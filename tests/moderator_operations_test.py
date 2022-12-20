from src.database.session import SessionLocal
from src.models import Match
from src.crud import moderator_operations


session = SessionLocal()


def test_get_complete_match_data():
    test_match = Match(date='1980-1-1', match_round=-1, home_team_id=0, away_team_id=1)
    test_match.id = -1
    
    session.add(test_match)
    session.commit()

    match = moderator_operations.get_complete_match_data(match_id=test_match.id)

    session.query(Match).filter(Match.id == test_match.id).delete()
    session.commit()

    assert match.get('match_data', None).get('id', None) == test_match.id and \
           match.get('home_team', None)[0].get('country_id', None) == test_match.home_team_id and \
           match.get('away_team', None)[0].get('country_id', None) == test_match.away_team_id

    
