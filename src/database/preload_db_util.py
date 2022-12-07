import os
import pandas as pd
from werkzeug.security import generate_password_hash

from src import models
from src.database.session import SessionLocal
from src.core.config import admin_default_account
from src.utility.date_operations import date_format_changer
from src.path_structure import ASSETS_DIRECTORY_PATH


session = SessionLocal()

DATA_DIRECTORY_PATH = os.path.join(ASSETS_DIRECTORY_PATH, 'data')


def add_default_admin_user() -> None:
    test_sample_query = session.query(models.User).filter(models.User.name == admin_default_account.USER).scalar()
    if test_sample_query:
        return None

    default_admin_user = models.User(
        name=admin_default_account.USER,
        email=admin_default_account.MAIL,
        password=generate_password_hash(admin_default_account.PASSWORD, method='sha256'),
        role=2
    )

    session.add(default_admin_user)
    session.commit()


def get_group_id_dict(countries_dataframe: pd.DataFrame) -> dict:
    wc_groups = set(countries_dataframe['Group'])
    return {country: index for index, country in enumerate(wc_groups)}


def get_countries_id_dict(countries_dataframe: pd.DataFrame) -> dict:
    return {country: country_id for country, country_id in
            zip(countries_dataframe['Country'], countries_dataframe['country_id'])}


def add_group_table_data(groups_dict: dict) -> None:
    for country, country_id in groups_dict.items():
        new_group = models.Group(
            id=int(country_id),
            name=country
        )
        session.add(new_group)

    session.commit()


def add_country_table_data(countries_dataframe: pd.DataFrame) -> None:
    groups_id = get_group_id_dict(countries_dataframe)

    for row in countries_dataframe.itertuples():
        new_country = models.Country(
            id=int(row.country_id),
            country=row.Country,
            world_ranking=int(row.World_ranking),
            tournament_ranking=int(row.Tournament_ranking),
            group_id=int(groups_id[row.Group])
        )
        session.add(new_country)

    session.commit()


def add_player_table_data(players_dataframe: pd.DataFrame, countries_dataframe: pd.DataFrame) -> None:
    countries_id = get_countries_id_dict(countries_dataframe)

    for row in players_dataframe.itertuples():
        new_player = models.Player(
            id=int(row.player_id),
            name=row.FIFA_Popular_Name,
            number=int(row.Number),
            position=row.Position,
            birth_date=date_format_changer(row.Birth_Date, '.', '-'),
            country_id=int(countries_id[row.Team])
        )
        session.add(new_player)

    session.commit()


def add_default_lineup_limits_table_data() -> None:
    active_lineup_limits = models.LineupLimits(gk=1, df=5, mf=5, fw=3, lineup_status='active')
    full_lineup_limits = models.LineupLimits(gk=2, df=7, mf=7, fw=5, lineup_status='full')

    session.bulk_save_objects([active_lineup_limits, full_lineup_limits])
    session.commit()
