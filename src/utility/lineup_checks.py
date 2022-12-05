from collections import Counter


MAX_NUMBER_OF_PLAYERS_IN_LINEUP = 20
ACTIVE_LINEUP_POSITION_COUNTER = {
        'GK': 1,
        'DF': 4,
        'MF': 5,
        'FW': 3
    }


def position_counter_check(players_lineup: list, max_positions_values: dict) -> bool:
    print(max_positions_values)
    position_counter = Counter()

    for player in players_lineup:
        position_counter.update({player.get('position', None): 1})
    print(position_counter)

    for position, number_of_players in position_counter.items():
        if number_of_players > max_positions_values.get(position, MAX_NUMBER_OF_PLAYERS_IN_LINEUP):
            return False
    return True


def country_counter_check(players_lineup: list, max_country_value: int) -> bool:
    print(max_country_value)
    country_counter = Counter()

    for player in players_lineup:
        country_counter.update({player.get('country_id', None): 1})
    print(country_counter)
    if not country_counter.values():
        return True
    return max(country_counter.values()) <= max_country_value


def active_lineup_values_check(players_lineup: list) -> bool:
    active_lineup_players = [player for player in players_lineup if player.get('active', False)]
    print(active_lineup_players)
    return len(players_lineup) == 11 and position_counter_check(players_lineup=active_lineup_players,
                                                                max_positions_values=ACTIVE_LINEUP_POSITION_COUNTER)
