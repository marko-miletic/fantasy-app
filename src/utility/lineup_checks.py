from collections import Counter

from src.crud.lineup_operations import get_lineup_limits


ACTIVE_LINEUP_SIZE = 11
MAX_NUMBER_OF_PLAYERS_PER_COUNTRY = 5


def max_lineup_size(players_lineup: list) -> bool:
    return len(players_lineup) <= sum(get_lineup_limits(status='full').values())


def position_counter_check(players_lineup: list, max_positions_values: dict) -> bool:
    print(max_positions_values)
    position_counter = Counter()

    for player in players_lineup:
        position_counter.update({player.get('position', None): 1})
    print(position_counter)

    for position, number_of_players in position_counter.items():
        if number_of_players > max_positions_values.get(position, sum(get_lineup_limits(status='full').values())):
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
    return len(active_lineup_players) <= ACTIVE_LINEUP_SIZE and \
           position_counter_check(players_lineup=active_lineup_players,
                                  max_positions_values=get_lineup_limits(status='active'))


def active_lineup_full_check(players_lineup: list) -> bool:
    active_lineup_players = [player for player in players_lineup if player.get('active', False)]
    return len(active_lineup_players) == ACTIVE_LINEUP_SIZE


def all_new_player_checks(players_lineup: list, max_position_values: dict) -> bool:
    return max_lineup_size(players_lineup) and \
           position_counter_check(players_lineup, max_position_values) and \
           country_counter_check(players_lineup, MAX_NUMBER_OF_PLAYERS_PER_COUNTRY) and \
           active_lineup_values_check(players_lineup)
