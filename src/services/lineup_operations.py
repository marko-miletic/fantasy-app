from src.database.session import SessionLocal

from src.models.player import Player
from src.models.selected_players import SelectedPlayers

from sqlalchemy import and_


session = SessionLocal()


def get_lineup(user_id: int, active: bool = False):

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

    lineup = session.query(
        Player.name,
        Player.number,
        Player.position,
        Player.country_id,
        SelectedPlayers.active
    ).join(SelectedPlayers).filter(active_query_switch.get(active, False)).all()
    lineup_data = [dict(zip(lineup_template, tuple(row))) for row in lineup]
    print(lineup_data)
    return lineup_data
