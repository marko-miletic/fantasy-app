from src.database.session import SessionLocal
from src.models import Player
from src.crud import player_operations


NUMBER_OF_PLAYERS = 736

session = SessionLocal()


def test_get_all_players():
    all_players = player_operations.get_all_players()

    assert len(all_players) == NUMBER_OF_PLAYERS and all_players[0].get('id') == 0


def test_get_players_by_country():
    country_players = player_operations.get_players_by_country(country_id=0)

    assert  len(country_players) != 0 and \
            len(list(filter(lambda player: player.get('country_id', -1) != 0, country_players))) == 0


def test_get_player_by_id():
    test_player = Player(id=-1, name='test', number=-1, position='test', birth_date='1980-1-1', country_id=0)

    session.add(test_player)
    session.commit()

    player = player_operations.get_player_by_id(player_id=test_player.id)

    session.query(Player).filter(Player.id == test_player.id).delete()
    session.commit()

    assert player is not None and player.get('id', None) == test_player.id
