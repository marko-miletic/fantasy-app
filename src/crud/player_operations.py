from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models import Player, Country


session = SessionLocal()

PLAYERS_TEMPLATE = [
    'id',
    'name',
    'number',
    'position',
    'country_id',
    'country'
]


def get_base_player_query() -> str:
    player_query = session.query(
        Player.id,
        Player.name,
        Player.number,
        Player.position,
        Country.id,
        Country.country
    )\
        .join(Country)
    return player_query


def get_all_players() -> list:
    try:
        players = get_base_player_query().all()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    players_data = [dict(zip(PLAYERS_TEMPLATE, tuple(row))) for row in players]
    return players_data


def get_players_by_country(country_id: int) -> list:
    try:
        players = get_base_player_query().filter(Country.id == country_id).all()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    players_data = [dict(zip(PLAYERS_TEMPLATE, tuple(row))) for row in players]
    return players_data


def get_player_by_id(player_id: int) -> dict:
    try:
        player = get_base_player_query().filter(Player.id == player_id).first()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    if player is None:
        logger.logging.error('Error Message', stack_info=True)
        raise ValueError(f'non existing data for given input: player_id: {player_id}')

    return dict(zip(PLAYERS_TEMPLATE, player))
