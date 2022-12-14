from sqlalchemy import or_
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models import Match, Country
from sqlalchemy.orm import aliased


session = SessionLocal()


def get_matches_by_status(status: str = 'all') -> list:
    match_status_switch = {
        'all': or_(Match.confirmed == True, Match.confirmed == False),  # all matches
        'confirmed': Match.confirmed == True,  # finished matches
        'active': Match.confirmed == False  # active_matches
    }

    matches_template = [
        'date',
        'round',
        'home_team_id',
        'home_team',
        'away_team_id',
        'away_team',
        'home_team_score',
        'away_team_score',
        'confirmed'
    ]

    try:
        home_country = aliased(Country)
        away_country = aliased(Country)
        matches = session.query(
            Match.date,
            Match.round,
            Match.home_team_id,
            home_country.country,
            Match.away_team_id,
            away_country.country,
            Match.home_score,
            Match.away_score,
            Match.confirmed
        )\
            .join(home_country, home_country.id == Match.home_team_id)\
            .join(away_country, away_country.id == Match.away_team_id)\
            .filter(match_status_switch.get(status, 'all')).all()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    matches_data = [dict(zip(matches_template, tuple(row))) for row in matches]
    return matches_data


def get_matches_by_round(match_round: int) -> list:
    matches_template = [
        'date',
        'round',
        'home_team_id',
        'home_team',
        'away_team_id',
        'away_team',
        'home_team_score',
        'away_team_score',
        'confirmed'
    ]

    try:
        home_country = aliased(Country)
        away_country = aliased(Country)
        matches = session.query(
            Match.date,
            Match.round,
            Match.home_team_id,
            home_country.country,
            Match.away_team_id,
            away_country.country,
            Match.home_score,
            Match.away_score,
            Match.confirmed
        )\
            .join(home_country, home_country.id == Match.home_team_id)\
            .join(away_country, away_country.id == Match.away_team_id)\
            .filter(Match.round == match_round)\
            .all()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    matches_data = [dict(zip(matches_template, tuple(row))) for row in matches]
    return matches_data


def get_match_count_by_round(match_round) -> int:
    try:
        match_count = session.query(func.count(Match.id))\
            .filter(Match.round == match_round)\
            .scalar()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    return match_count


def post_create_new_match(date: str, match_round: int, home_team_id: int, away_team_id):
    new_match = Match(date=date, match_round=match_round, home_team_id=home_team_id, away_team_id=away_team_id)

    try:
        session.add(new_match)
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err


def update_change_match_status(match_id: int, new_status: str = 'confirmed'):
    status_switch = {
        'confirmed': True,
        'active': False
    }

    try:
        session.query(Match)\
            .filter(Match.id == match_id)\
            .update({Match.confirmed: status_switch.get(new_status, False)})
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err
