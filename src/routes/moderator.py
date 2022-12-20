from flask import Blueprint, request, make_response, redirect, url_for, flash, render_template
from flask_login import current_user

from src.core.roles import merged_login_role_required_decorator
from src.logs import logger
from src.crud import moderator_operations
from src.path_structure import TEMPLATES_DIRECTORY_PATH


moderator = Blueprint('moderator', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@moderator.route('/', methods=['GET'])
@merged_login_role_required_decorator(role_value='moderator')
def moderator_index():
    return make_response({'status': 200, 'profile_info': current_user})


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
def moderator_complete_match_get(match_id: int):
    try:
        match = moderator_operations.get_complete_match_data(match_id=match_id)
        return render_template(
            'match-complete.html',
            match_data=match.get('match_data', None),
            home_team=match.get('home_team', None),
            away_team=match.get('away_team', None)
        )
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while loading match data')
        return redirect(url_for('moderator.moderator_active_matches'))


@moderator.route('/complete-match/<int:match_id>', methods=['POST'])
@merged_login_role_required_decorator(role_value='moderator')
def moderator_complete_match_post(match_id: int):
    try:
        match = moderator_operations.get_complete_match_data(match_id=match_id)
        home_team_points_score = 0
        for home_player in match.get('home_team', None):
            home_team_points_score += int(request.form[str(home_player.get('id', None))])
        away_team_points_score = 0
        for away_player in match.get('home_team', None):
            away_team_points_score += int(request.form[str(away_player.get('id', None))])
        return make_response({'home_score': home_team_points_score, 'away_score': away_team_points_score})
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while loading match data')
        return redirect(url_for('moderator.moderator_active_matches'))