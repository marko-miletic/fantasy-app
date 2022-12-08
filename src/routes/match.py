from flask import Blueprint, make_response, redirect, url_for
# from flask_login import login_required, current_user

from src.services import match_operations
from src.path_structure import TEMPLATES_DIRECTORY_PATH


match = Blueprint('match', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@match.route('/', methods=['GET'])
@match.route('/all', methods=['GET'])
def all_matches():
    matches = match_operations.get_matches_by_status(status=0)
    return make_response(matches)


# test route for creating new match
@match.route('/create-new/<int:home_team_id>/<int:away_team_id>', methods=['GET'])
def create_new_match(home_team_id: int, away_team_id: int):
    match_operations.post_create_new_match(date='1980-1-1', home_team_id=home_team_id, away_team_id=away_team_id)
    return redirect(url_for('match.all_matches'))


# test route for updating match status
@match.route('/change-status/<int:match_id>/<string:new_status>', methods=['GET'])
def update_match_status(match_id: int, new_status: str):
    match_operations.update_change_match_status(match_id=match_id, new_status=bool(new_status))
    return redirect(url_for('match.all_matches'))
