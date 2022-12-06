from src.database.session import SessionLocal

from src.models.player import Player
from src.models.country import Country


session = SessionLocal()


def get_all_players():

    players_template = [
        'id',
        'name',
        'number',
        'position',
        'country'
    ]

    players = session.query(
        Player.id,
        Player.name,
        Player.number,
        Player.position,
        Country.country
    ).join(Country).all()
    players_data = [dict(zip(players_template, tuple(row))) for row in players]
    return players_data
