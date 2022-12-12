import logging
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from src.database.session import SessionLocal
from src.models import Player, SelectedPlayers, LineupLimits


session = SessionLocal()


def add_player_to_lineup(user_id: int, player_id: int):
    try:
        new_lineup_player = SelectedPlayers(user_id=user_id, player_id=player_id)
        session.add(new_lineup_player)
        session.commit()
    except SQLAlchemyError as err:
        logging.error(err)
        raise err


def get_lineup(user_id: int, active: bool = False) -> list:
    active_query_switch = {
        True: and_(SelectedPlayers.user_id == user_id, SelectedPlayers.active == True),
        False: SelectedPlayers.user_id == user_id
    }

    lineup_template = [
        'name',
        'number',
        'position',
        'country_id',
        'active'
    ]

    try:
        lineup = session.query(
            Player.name,
            Player.number,
            Player.position,
            Player.country_id,
            SelectedPlayers.active
        )\
            .join(SelectedPlayers)\
            .filter(active_query_switch.get(active, False))\
            .all()
    except SQLAlchemyError as err:
        logging.error(err)
        raise err

    lineup_data = [dict(zip(lineup_template, tuple(row))) for row in lineup]
    return lineup_data


def get_lineup_limits(status: str) -> dict:
    lineup_limits_template = [
        'GK',
        'DF',
        'MF',
        'FW'
    ]

    try:
        lineup_limits = session.query(
            LineupLimits.gk,
            LineupLimits.df,
            LineupLimits.mf,
            LineupLimits.fw
        )\
            .filter(LineupLimits.lineup_status == status)\
            .first()
    except SQLAlchemyError as err:
        logging.error(err)
        raise err

    if lineup_limits is None:
        logging.error('Error Message', stack_info=True)
        raise ValueError(f'non existing data for lineup limits: status: {status}')

    return dict(zip(lineup_limits_template, lineup_limits))
