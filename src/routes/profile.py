from flask import Blueprint, make_response, redirect, url_for, flash
from flask_login import login_required, current_user

from src.logs import logger
from src.crud import points_operations
from src.path_structure import TEMPLATES_DIRECTORY_PATH


profile = Blueprint('profile', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@profile.route('/', methods=['GET'])
@login_required
def profile_index():
    try:
        # total_points_count = points_operations.get_points_per_user(user_id=current_user.id)
        return make_response({'user': current_user.id}), 200
    except Exception as err:
        logger.logging.error(err)
        flash('An logs occurred while loading profile')
        return redirect(url_for('index.main'))


@profile.route('/points/round/<int:round_number>', methods=['GET'])
@login_required
def user_round_points(round_number: int):
    try:
        total_points_count = points_operations.get_points_per_user_per_round(user_id=current_user.id,
                                                                             round_number=round_number)
        return make_response({'round': round_number, 'points': total_points_count}), 200
    except Exception as err:
        logger.logging.error(err)
        flash('An logs occurred while loading points per round page')
        return redirect(url_for('profile.profile_index'))
