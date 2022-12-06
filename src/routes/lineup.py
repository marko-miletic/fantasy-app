from flask import (
    Blueprint,
    make_response
)

from flask_login import (
    login_required,
    current_user
)

from src.services.lineup_operations import get_lineup

from src.utility.lineup_checks import (
    position_counter_check,
    country_counter_check,
    active_lineup_values_check
)

from src.path_structure import TEMPLATES_DIRECTORY_PATH


lineup = Blueprint('lineup', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@lineup.route('/full')
@login_required
def lineup_all():
    lineup_data = get_lineup(user_id=current_user.id, active=False)

    test_values = {
        'GK': 2,
        'DF': 5,
        'MF': 3,
        'FW': 4
    }

    print(position_counter_check(lineup_data, test_values))
    print(country_counter_check(lineup_data, 5))
    print(active_lineup_values_check(lineup_data))
    return make_response(lineup_data)


@lineup.route('/active')
@login_required
def lineup_active():
    lineup_data = get_lineup(user_id=current_user.id, active=True)

    return make_response(lineup_data)
