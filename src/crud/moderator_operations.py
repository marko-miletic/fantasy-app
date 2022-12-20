from src.logs import logger
from src.database.session import SessionLocal
from src.crud.match_operations import get_matches_by_status, get_match_by_id
from src.crud.player_operations import get_players_by_country


session = SessionLocal()


def get_active_matches() -> list:
    return get_matches_by_status(status='active')


def get_complete_match_data(match_id: int) -> dict:
    try:
        match_data = get_match_by_id(match_id=match_id)
        home_team_players = get_players_by_country(match_data.get('home_team_id', None))
        away_team_players = get_players_by_country(match_data.get('away_team_id', None))
    except ValueError as err:
        logger.logging.error(err)
        raise err
    if not all([match_data, home_team_players, away_team_players]):
        logger.logging.error('Error Message', stack_info=True)
        raise ValueError(f'incomplete data for given match_id: {match_id}')
    return {
        'match_data': match_data,
        'home_team': home_team_players,
        'away_team': away_team_players
    }
