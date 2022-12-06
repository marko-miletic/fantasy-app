from collections import defaultdict

from flask import (
    Blueprint,
    make_response,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from src import services

from src.utility.lineup_checks import all_new_player_checks
from src.services.lineup_operations import add_player_to_lineup

from src.path_structure import TEMPLATES_DIRECTORY_PATH


lineup = Blueprint('lineup', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@lineup.route('/', methods=['GET'])
@lineup.route('/full', methods=['GET'])
@login_required
def lineup_all():
    lineup_data = services.lineup_operations.get_lineup(user_id=current_user.id, active=False)

    test_values = {
        'GK': 2,
        'DF': 5,
        'MF': 3,
        'FW': 4
    }

    all_new_player_checks(lineup_data, test_values)
    return make_response(lineup_data)


@lineup.route('/active', methods=['GET'])
@login_required
def lineup_active():
    lineup_data = services.lineup_operations.get_lineup(user_id=current_user.id, active=True)

    return make_response(lineup_data)


@lineup.route('/add-player', methods=['GET'])
@login_required
def list_players():
    current_lineup_players = services.lineup_operations.get_lineup(user_id=current_user.id,
                                                                   active=False)
    selected_players_set = set([player['name'] for player in current_lineup_players])

    all_players = services.player_operations.get_all_players()
    filtered_unselected_players = defaultdict(list)
    for player in all_players:
        if player.get('name', None) not in selected_players_set:
            filtered_unselected_players[player.get('country', None)].append(player)

    return make_response(filtered_unselected_players)


@lineup.route('/add-player/<int:player_id>', methods=['GET'])
@login_required
def add_player(player_id: int):
    test_values = {
        'GK': 2,
        'DF': 5,
        'MF': 3,
        'FW': 4
    }
    add_player_to_lineup(current_user.id, player_id)
    return redirect(url_for('lineup.lineup_all'))
