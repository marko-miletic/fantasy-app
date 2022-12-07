from src.database.session import SessionLocal
from src.core.config import admin_default_account
from src.models import Group, Country, Player, User, LineupLimits


session = SessionLocal()


def test_database_admin_user():
    admin = session.query(User).filter(User.name == admin_default_account.USER).scalar()

    assert admin is not None


def test_get_group_by_id():
    test_group = Group(id=-1, name='T')

    session.add(test_group)
    session.commit()

    group = session.query(Group).filter(Group.id == test_group.id).first()

    session.query(Group).filter(Group.id == test_group.id).delete()
    session.commit()

    assert group is not None


def test_get_country_by_id():
    test_country = Country(id=-1, country='test', world_ranking=-1, tournament_ranking=-1, group_id=0)

    session.add(test_country)
    session.commit()

    country = session.query(Country).filter(Country.id == test_country.id).first()

    session.query(Country).filter(Country.id == test_country.id).delete()
    session.commit()

    assert country is not None


def test_get_player_by_id():
    test_player = Player(id=-1, name='test', number=-1, position='test', birth_date='1980-1-1', country_id=0)

    session.add(test_player)
    session.commit()

    player = session.query(Player).filter(Player.id == test_player.id).first()

    session.query(Player).filter(Player.id == test_player.id).delete()
    session.commit()

    assert player is not None


def test_data_prefilled():
    admin = session.query(User).filter(User.name == admin_default_account.USER).scalar()
    group = session.query(Group).filter(Group.id == 0).first()
    country = session.query(Country).filter(Country.id == 0).first()
    player = session.query(Player).filter(Player.id == 0).first()
    lineup_limits = session.query(LineupLimits).filter(LineupLimits.id == 1).first()

    assert all([admin, group, country, player, lineup_limits])
