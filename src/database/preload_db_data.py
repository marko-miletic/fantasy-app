import os
import pandas as pd

from src.database.session import SessionLocal

from src.database.preload_db_util import add_group_table_data
from src.database.preload_db_util import add_player_table_data
from src.database.preload_db_util import add_country_table_data
from src.database.preload_db_util import add_default_admin_user
from src.database.preload_db_util import get_group_id_dict

from src.models.group import Group

from src.path_structure import ASSETS_DIRECTORY_PATH


session = SessionLocal()

DATA_DIRECTORY_PATH = os.path.join(ASSETS_DIRECTORY_PATH, 'data')


def fill_db_data() -> None:
    
    add_default_admin_user()

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

    add_group_table_data(get_group_id_dict(countries_dataframe))
    add_country_table_data(countries_dataframe)
    add_player_table_data(players_dataframe, countries_dataframe)
