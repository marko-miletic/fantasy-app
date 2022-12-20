from flask import Blueprint, make_response, redirect, url_for, flash
from flask_login import login_required, current_user

from src.core.roles import merged_login_role_required_decorator
from src.logs import logger
from src.crud import moderator_operations
from src.utility import match_checks
from src.path_structure import TEMPLATES_DIRECTORY_PATH


moderator = Blueprint('moderator', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@moderator.route('/', methods=['GET'])
@merged_login_role_required_decorator(role_value='moderator')
def moderator_index():
    return make_response({'status': 200, 'role': current_user.role})


@moderator.route('/active-matches', methods=['GET'])
@merged_login_role_required_decorator(role_value='moderator')
def moderator_active_matches():
    try:
        active_matches = moderator_operations.get_active_matches()
        return make_response(active_matches)
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while loading active matches')
        return redirect(url_for('moderator.moderator_index'))


@moderator.route('/complete-match/<int:match_id>', methods=['GET'])
@merged_login_role_required_decorator(role_value='moderator')
def moderator_complete_match(match_id: int):
    try:
        match = moderator_operations.get_complete_match_data(match_id=match_id)
        return make_response({
            'match_data': match.get('match_data', None),
            'home_team': match.get('home_team', None),
            'away_team': match.get('away_team', None)
        })
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while loading match data')
        return redirect(url_for('moderator.moderator_active_matches'))
