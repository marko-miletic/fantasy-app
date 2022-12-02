from src.models.user import User
from src.database.session import SessionLocal
from src.core.config import admin_default_account

from src.models.group import Group
from src.models.country import Country
from src.models.player import Player


session = SessionLocal()


TEST_GROUP = Group(id=-1, name='T')

TEST_COUNTRY = Country(id=-1, country='test', world_ranking=-1, tournament_ranking=-1, group_id=0)

TEST_PLAYER = Player(id=-1, name='test', number=-1, position='test', birth_date='1980-1-1', country_id=0)


def test_database_admin_user():
    admin = session.query(User).filter(User.name == admin_default_account.USER).scalar()
    assert admin is not None


def test_get_group_by_id():
    session.add(TEST_GROUP)
    session.commit()

    group = session.query(Group).filter(Group.id == TEST_GROUP.id).first()

    session.query(Group).filter(Group.id == TEST_GROUP.id).delete()
    session.commit()

    assert group is not None


def test_get_country_by_id():
    session.add(TEST_COUNTRY)
    session.commit()

    country = session.query(Country).filter(Country.id == TEST_COUNTRY.id).first()

    session.query(Country).filter(Country.id == TEST_COUNTRY.id).delete()
    session.commit()

    assert country is not None


def test_get_player_by_id():
    session.add(TEST_PLAYER)
    session.commit()

    player = session.query(Player).filter(Player.id == TEST_PLAYER.id).first()

    session.query(Player).filter(Player.id == TEST_PLAYER.id).delete()
    session.commit()

    assert player is not None


def test_data_prefilled():
    group = session.query(Group).filter(Group.id == 0).first()
    country = session.query(Country).filter(Country.id == 0).first()
    player = session.query(Player).filter(Player.id == 0).first()
    assert all([group, country, player])
