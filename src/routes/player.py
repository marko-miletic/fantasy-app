from flask import (
    Blueprint,
    render_template,
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


player = Blueprint('player', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@player.route('/lineup')
@login_required
def main():
    lineup = get_lineup(user_id=current_user.id)

    test_values = {
        'GF': 2,
        'DF': 5,
        'MF': 3,
        'FW': 4
    }

    print(position_counter_check(lineup, test_values))
    print(country_counter_check(lineup, 5))
    return make_response(lineup)
