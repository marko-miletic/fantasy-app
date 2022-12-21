from flask import Blueprint, request, make_response, redirect, url_for, flash, render_template
from flask_login import current_user

from src.core.roles import merged_login_role_required_decorator
from src.logs import logger
from src.crud import moderator_operations, auth_operations, points_operations, match_operations
from src.utility.moderator_points_utility import define_player_points_and_goals_per_match
from src.utility.match_checks import check_round_finished_status
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

        for home_player in match.get('home_team', None):
            home_player_id = home_player.get('id', None)
            define_player_points_and_goals_per_match(opposite_team_score=int(request.form['away_team_score']),
                                                     player_score=int(request.form[f'goals_{home_player_id}']),
                                                     player_assists=int(request.form[f'assists_{home_player_id}']),
                                                     player_cards=int(request.form[f'cards_{home_player_id}']),
                                                     player_minutes=int(request.form[f'minutes_{home_player_id}']),
                                                     player=home_player,
                                                     match_id=match_id)

        for away_player in match.get('away_team', None):
            away_player_id = away_player.get('id', None)
            define_player_points_and_goals_per_match(opposite_team_score=int(request.form['home_team_score']),
                                                     player_score=int(request.form[f'goals_{away_player_id}']),
                                                     player_assists=int(request.form[f'assists_{away_player_id}']),
                                                     player_cards=int(request.form[f'cards_{away_player_id}']),
                                                     player_minutes=int(request.form[f'minutes_{away_player_id}']),
                                                     player=away_player,
                                                     match_id=match_id)

        # match_operations.update_change_match_status(match_id=match.get('id'), None)

        if check_round_finished_status(match_round=match.get('round', None)):
            users = auth_operations.get_all_users_ids()
            for user_id in users:
                user_round_points = points_operations.get_sum_user_round_points(user_id=user_id, 
                                                                                round_number=match.get('round', None))
                points_operations.post_user_points_for_given_round(user_id=user_id,
                                                                   round_number=match.get('round', None),
                                                                   points_count=user_round_points)
        return make_response({'status': 200})
    except Exception as err:
        logger.logging.error(err)
        flash('An error occurred while loading match data')
        return redirect(url_for('moderator.moderator_active_matches'))
