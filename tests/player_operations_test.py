from src.database.session import SessionLocal
from src.models import Player
from src.crud import player_operations


NUMBER_OF_PLAYERS = 736

session = SessionLocal()


def test_get_all_players():
    all_players = player_operations.get_all_players()

    assert len(all_players) == NUMBER_OF_PLAYERS and all_players[0].get('id') == 0


def test_get_player_by_id():
    test_player = Player(id=-1, name='test', number=-1, position='test', birth_date='1980-1-1', country_id=0)

    session.add(test_player)
    session.commit()

    player = player_operations.get_player_by_id(test_player.id)

    session.query(Player).filter(Player.id == test_player.id).delete()
    session.commit()

    assert player is not None


def test_get_player_by_nonexistent_id():
    non_existing_player_id = -1

    player = player_operations.get_player_by_id(non_existing_player_id)

    assert player is None
