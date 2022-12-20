from flask import Blueprint, make_response, redirect, url_for, flash
from flask_login import login_required, current_user

from src.logs import logger
from src.crud import admin_operations
from src.core.roles import role_required, role_names, merged_login_role_required_decorator
from src.path_structure import TEMPLATES_DIRECTORY_PATH


admin = Blueprint('admin', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@admin.route('', methods=['GET'])
@merged_login_role_required_decorator(role_value='admin')
def admin_index():
    return make_response({'user_id': current_user.id, 'status': 200})


@admin.route('/update-user-status/<int:user_id>/<string:new_role>', methods=['GET'])
@merged_login_role_required_decorator(role_value='admin')
def update_user_status(user_id: int, new_role: str):
    try:
        print()
        admin_operations.update_change_user_status(new_role=new_role, user_id=user_id)
        return redirect(url_for('admin.admin_index'))
    except Exception as err:
        logger.logging.error(err)
        flash('An logs occurred while loading matches')
        return redirect(url_for('index.main'))
