from src.database.session import SessionLocal
from src.models import User, Match, SelectedPlayers
from src.crud import auth_operations, lineup_operations
from src.utility import date_operations, lineup_checks, match_checks


session = SessionLocal()


def test_date_format_changer():
    input_date_space = '1 1 1980'
    input_date_comma = '1,1,1980'
    formatted_output = '1980-1-1'

    assert date_operations.date_format_changer(input_date_space, ' ', '-') == formatted_output and \
           date_operations.date_format_changer(input_date_comma, ',', '-') == formatted_output


def test_all_new_player_checks():
    test_user = User(name='test', email='test', password='test')
    test_user.id = -1

    auth_operations.post_create_new_user(test_user)
    lineup_operations.add_player_to_lineup(test_user.id, 0)

    test_lineup = lineup_operations.get_lineup(test_user.id)

    session.query(SelectedPlayers).filter(SelectedPlayers.user_id == test_user.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert lineup_checks.all_new_player_checks(test_lineup, lineup_operations.get_lineup_limits(status='full')) is True


def test_check_playing_teams_by_round():
    test_match = Match(date='1980-1-1', match_round=-1, home_team_id=0, away_team_id=1)
    test_match.id = -1

    session.add(test_match)
    session.commit()

    home_team_status = match_checks.check_playing_teams_by_round((0, 2), match_round=test_match.round)
    away_team_status = match_checks.check_playing_teams_by_round((2, 1), match_round=test_match.round)
    available_match_status = match_checks.check_playing_teams_by_round((2, 3), match_round=test_match.round)

    session.query(Match).filter(Match.id == test_match.id).delete()
    session.commit()

    assert home_team_status is False and away_team_status is False and available_match_status is True
