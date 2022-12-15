from src.logs import logger
from src.crud.match_operations import get_matches_by_round, get_match_count_by_round
from src.crud.country_operations import get_countries_count


def check_playing_teams_by_round(match_teams: tuple, match_round: int) -> bool:  # tuple(home_team, away_team)
    try:
        matches_assigned_by_round = get_matches_by_round(match_round)
        active_teams = set()
        for match in matches_assigned_by_round:
            active_teams.add(match.get('home_team_id'))
            active_teams.add(match.get('away_team_id'))
    except Exception as err:
        logger.logging.error(err)
        raise err
    return match_teams[0] not in active_teams and match_teams[1] not in active_teams


def check_round_finished_status(match_round: int) -> bool:
    try:
        match_count = get_match_count_by_round(match_round=match_round)
        if match_count == 0:
            return False
        countries_count = get_countries_count()
    except Exception as err:
        logger.logging.error(err)
        raise err
    return countries_count // match_count == 2


def all_new_match_checks(match_round: int, home_team_id: int, away_team_id: int):
    try:
        return check_playing_teams_by_round((home_team_id, away_team_id), match_round) and \
            not check_round_finished_status(match_round)
    except Exception as err:
        logger.logging.error(err)
        raise err
