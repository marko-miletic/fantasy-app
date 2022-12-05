from src.database.session import SessionLocal

from src.models.player import Player
from src.models.selected_players import SelectedPlayers


session = SessionLocal()


def get_lineup(user_id: int):
    lineup_template = [
        'name',
        'number',
        'position',
        'country_id'
    ]
    lineup = session.query(
        Player.name,
        Player.number,
        Player.position,
        Player.country_id
    ).join(SelectedPlayers).filter(SelectedPlayers.user_id == user_id).all()
    lineup_data = [dict(zip(lineup_template, tuple(row))) for row in lineup]
    return lineup_data
