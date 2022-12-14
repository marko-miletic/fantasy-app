from sqlalchemy import and_, desc
from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models import League, UserLeague, User


session = SessionLocal()

LEAGUE_TEMPLATE = [
    'id',
    'name',
    'current_round',
    'owner_id'
]


def post_create_new_league(league_name: str, owner_id) -> None:
    try:
        new_league = League(name=league_name, owner_id=owner_id)
        session.add(new_league)
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err


def get_league_by_id(league_id: int) -> dict:
    try:
        league = session.query(
            League.id,
            League.name,
            League.current_round,
            League.owner_id
        )\
            .filter(League.id == league_id)\
            .first()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    if league is None:
        logger.logging.error('Error Message', stack_info=True)
        raise ValueError(f'non existing data for league data: league_id: {league_id}')

    return dict(zip(LEAGUE_TEMPLATE, league))


def get_league_by_owner(owner_id: int) -> list:
    try:
        leagues = session.query(
            League.id,
            League.name,
            League.current_round,
            League.owner_id
        )\
            .filter(League.owner_id == owner_id)\
            .all()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    leagues_data = [dict(zip(LEAGUE_TEMPLATE, tuple(row))) for row in leagues]
    return leagues_data


def get_leagues_by_user(user_id: int) -> list:
    try:
        leagues = session.query(
            League.id,
            League.name,
            League.current_round,
            League.owner_id
        )\
            .join(UserLeague)\
            .filter(UserLeague.user_id == user_id)\
            .all()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    leagues_data = [dict(zip(LEAGUE_TEMPLATE, tuple(row))) for row in leagues]
    return leagues_data


def get_league_rankings_by_league_id(league_id: int) -> list:
    league_ranking_template = [
        'user_id',
        'name',
        'email',
        'points'
    ]

    try:
        league_players = session.query(
            User.id,
            User.name,
            User.email,
            UserLeague.points
        )\
            .join(UserLeague)\
            .filter(UserLeague.league_id == league_id)\
            .order_by(desc(UserLeague.points))\
            .all()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    league_ranking = [dict(zip(league_ranking_template, tuple(row))) for row in league_players]
    return league_ranking


def update_approve_new_league_player(league_id: int, user_id: int) -> None:
    try:
        session.query(UserLeague)\
            .filter(and_(UserLeague.league_id == league_id, UserLeague.user_id == user_id))\
            .update({UserLeague.approved_access: True})
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err
