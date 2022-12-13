from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models import Player, Country


session = SessionLocal()


def get_all_players() -> list:
    players_template = [
        'id',
        'name',
        'number',
        'position',
        'country'
    ]

    try:
        players = session.query(
            Player.id,
            Player.name,
            Player.number,
            Player.position,
            Country.country
        )\
            .join(Country)\
            .all()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    players_data = [dict(zip(players_template, tuple(row))) for row in players]
    return players_data


def get_player_by_id(player_id: int) -> dict:
    player_template = [
        'name',
        'number',
        'position',
        'country_id'
    ]

    try:
        player = session.query(
            Player.name,
            Player.number,
            Player.position,
            Player.country_id
        )\
            .filter(Player.id == player_id)\
            .first()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    if player is None:
        logger.logging.error('Error Message', stack_info=True)
        raise ValueError(f'non existing data for given input: player_id: {player_id}')

    return dict(zip(player_template, player))
