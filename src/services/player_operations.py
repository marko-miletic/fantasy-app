from src.database.session import SessionLocal
from src.models import Player, Country


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


def get_player_by_id(player_id: int) -> dict:
    player_template = [
        'name',
        'number',
        'position',
        'country_id'
    ]

    player = session.query(
        Player.name,
        Player.number,
        Player.position,
        Player.country_id
    ).filter(Player.id == player_id).first()

    return dict(zip(player_template, player))
