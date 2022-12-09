import logging
from collections import defaultdict
from flask import Blueprint, make_response, redirect, url_for, flash
from flask_login import login_required, current_user

from src.crud import lineup_operations, player_operations
from src.utility.lineup_checks import all_new_player_checks
from src.path_structure import TEMPLATES_DIRECTORY_PATH


lineup = Blueprint('lineup', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@lineup.route('/', methods=['GET'])
@lineup.route('/full', methods=['GET'])
@login_required
def lineup_all():
    lineup_data = lineup_operations.get_lineup(user_id=current_user.id, active=False)

    full_lineup_limits = lineup_operations.get_lineup_limits('full')
    all_new_player_checks(lineup_data, full_lineup_limits)
    return make_response(lineup_data)


@lineup.route('/active', methods=['GET'])
@login_required
def lineup_active():
    try:
        lineup_data = lineup_operations.get_lineup(user_id=current_user.id, active=True)

        return make_response(lineup_data)
    except Exception as err:
        logging.error(err)
        flash('An error occurred while loading lineup')
        return redirect(url_for('index.main'))


@lineup.route('/add-player', methods=['GET'])
@login_required
def list_players():
    try:
        current_lineup_players = lineup_operations.get_lineup(user_id=current_user.id,
                                                              active=False)
        selected_players_set = set([player['name'] for player in current_lineup_players])

        all_players = player_operations.get_all_players()
        filtered_unselected_players = defaultdict(list)
        for player in all_players:
            if player.get('name', None) not in selected_players_set:
                filtered_unselected_players[player.get('country', None)].append(player)

        return make_response(filtered_unselected_players)
    except Exception as err:
        logging.error(err)
        flash('An error occurred while adding player to lineup')
        return redirect(url_for('lineup.lineup_active'))


@lineup.route('/add-player/<int:player_id>', methods=['GET'])
@login_required
def add_player(player_id: int):
    try:
        player = player_operations.get_player_by_id(player_id)
        player['active'] = False
        current_lineup_players = lineup_operations.get_lineup(user_id=current_user.id,
                                                              active=False)
        current_lineup_players.append(player)

        full_lineup_limits = lineup_operations.get_lineup_limits('full')
        if not all_new_player_checks(current_lineup_players, full_lineup_limits):
            flash('Lineup checks failed for given player')
            return redirect(url_for('lineup.list_players'))

        lineup_operations.add_player_to_lineup(current_user.id, player_id)
        return redirect(url_for('lineup.lineup_all'))
    except Exception as err:
        logging.error(err)
        flash('An error occurred while adding player to lineup')
        return redirect(url_for('lineup.lineup_active'))
