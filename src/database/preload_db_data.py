import os
import pandas as pd

from src import database

from src.models.group import Group

from src.path_structure import ASSETS_DIRECTORY_PATH


session = database.SessionLocal()

DATA_DIRECTORY_PATH = os.path.join(ASSETS_DIRECTORY_PATH, 'data')


def fill_db_data() -> None:
    
    database.add_default_admin_user()

    test_sample_query = session.query(Group).filter(Group.id == 0).scalar()
    if test_sample_query:
        return None

    countries_dataframe = pd.read_csv(os.path.join(DATA_DIRECTORY_PATH, 'wc2018-countries.csv'))
    countries_dataframe['country_id'] = countries_dataframe.index
    players_dataframe = pd.read_csv(os.path.join(DATA_DIRECTORY_PATH, 'wc2018-players.csv'))
    players_dataframe['player_id'] = players_dataframe.index

    players_dataframe_team_changes = {
        'IR Iran': 'Iran',
        'Korea Republic': 'South Korea'
    }

    players_dataframe['Team'] = players_dataframe['Team'].replace(
        players_dataframe_team_changes.keys(), players_dataframe_team_changes.values()
    )

    database.add_group_table_data(database.get_group_id_dict(countries_dataframe))
    database.add_country_table_data(countries_dataframe)
    database.add_player_table_data(players_dataframe, countries_dataframe)
