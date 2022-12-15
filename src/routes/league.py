from flask import Blueprint, make_response, redirect, url_for, flash, request
from flask_login import login_required, current_user

from src.logs import logger
from src.crud import league_operations
from src.utility import league_checks
from src.path_structure import TEMPLATES_DIRECTORY_PATH


league = Blueprint('league', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@league.route('/', methods=['GET'])
@login_required
def user_leagues():
    try:
        user_leagues_data = league_operations.get_leagues_by_user(user_id=current_user.id)

        return make_response(user_leagues_data)
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while loading user leagues')
        return redirect(url_for('profile.profile_index'))


@league.route('/created', methods=['GET'])
@login_required
def user_created_leagues():
    try:
        user_created_leagues_data = league_operations.get_league_by_owner(owner_id=current_user.id)
        
        return make_response(user_created_leagues_data)
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while loading user created leagues')
        return redirect(url_for('league.user_leagues'))


@league.route('/create-league/<string:league_name>', methods=['GET'])
@login_required
def create_new_league(league_name: str):
    try:
        league_operations.post_create_new_league(league_name=league_name, owner_id=current_user.id)

        return redirect(url_for('league.user_created_league'))
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while creating new league')
        return redirect(url_for('league.user_created_league'))


@league.route('/add-user/<int:league_id>/<int:user_id>', methods=['GET'])
@login_required
def add_new_user_to_league(league_id: int, user_id: int):
    try:
        league_operations.post_add_user_to_league(user_id=user_id, league_id=league_id)

        return redirect(url_for('league.league_by_id', league_id=league_id))
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while adding user to specific league')
        return redirect(url_for('league.league_by_id', league_id=league_id))


@league.route('/approve-player/<int:league_id>/<int:user_id>')
@login_required
def approve_league_player(league_id: int, user_id: int):
    try:
        if not league_checks.user_in_league_check(league_id=league_id, user_id=user_id):
            return redirect(request.url)

        league_operations.update_approve_new_league_player(league_id=league_id, user_id=user_id)

        return redirect(url_for('league.league_by_id', league_id=league_id))
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while trying to approve given player')
        return redirect(url_for('league.league_by_id', league_id=league_id))


@league.route('/<int:league_id>', methods=['GET'])
@login_required
def league_by_id(league_id: int):
    try:
        league_data = league_operations.get_league_by_id(league_id=league_id)

        return make_response(league_data)
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while loading league')
        return redirect(url_for('league.user_leagues'))


@league.route('/<int:league_id>/ranking', methods=['GET'])
@login_required
def league_by_id_ranking(league_id: int):
    try:
        league_data = league_operations.get_league_rankings_by_league_id(league_id=league_id)

        return make_response(league_data)
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while loading league ranking')
        return redirect(url_for('league.user_leagues'))
