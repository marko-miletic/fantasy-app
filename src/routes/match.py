import logging
from flask import Blueprint, make_response, redirect, url_for, flash
# from flask_login import login_required, current_user

from src.crud import match_operations
from src.path_structure import TEMPLATES_DIRECTORY_PATH


match = Blueprint('match', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@match.route('/', methods=['GET'])
@match.route('/all', methods=['GET'])
def all_matches():
    try:
        matches = match_operations.get_matches_by_status(status='all')
        return make_response(matches)
    except Exception as err:
        logging.error(err)
        flash('An error occurred while loading matches')
        return redirect(url_for('index.main'))


# test route for creating new match
@match.route('/create-new/<int:home_team_id>/<int:away_team_id>/<int:match_round>', methods=['GET'])
def create_new_match(match_round: int, home_team_id: int, away_team_id: int):
    try:
        match_operations.post_create_new_match(date='1980-1-1',
                                               match_round=match_round,
                                               home_team_id=home_team_id,
                                               away_team_id=away_team_id)
        return redirect(url_for('match.all_matches'))
    except Exception as err:
        logging.error(err)
        flash('An error occurred while creating new match')
        return redirect(url_for('match.all_matches'))


# test route for updating match status
@match.route('/change-status/<int:match_id>/<string:new_status>', methods=['GET'])
def update_match_status(match_id: int, new_status: str):
    try:
        match_operations.update_change_match_status(match_id=match_id, new_status=new_status)
        return redirect(url_for('match.all_matches'))
    except Exception as err:
        logging.error(err)
        flash('An error occurred while changing match status')
        return redirect(url_for('match.all_matches'))


@match.route('/round/<int:match_round>', methods=['GET'])
def matches_by_round(match_round: int):
    try:
        matches = match_operations.get_matches_by_round(match_round)
        return make_response(matches)
    except Exception as err:
        logging.error(err)
        flash('An error occurred while accessing matches by round')
        return redirect(url_for('match.all_matches'))
