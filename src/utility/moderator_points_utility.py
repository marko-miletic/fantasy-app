from src.crud.points_operations import post_player_goals_per_match, post_player_points_per_match


def count_points(opposite_team_score: int,
                 player_score: int,
                 player_assists: int,
                 player_cards: int,
                 player_minutes: int,
                 player: dict) -> int:
    points_count = 3 * player_score
    points_count += player_assists
    if player.get('position', None) == 'DF' and opposite_team_score == 0:
        points_count += 3
    if player_cards != 0:
        points_count -= 3
    if player_minutes > 60:
        points_count += 1
    return points_count


def define_player_points_and_goals_per_match(opposite_team_score: int,
                                             player_score: int,
                                             player_assists: int,
                                             player_cards: int,
                                             player_minutes: int,
                                             player: dict,
                                             match_id: int):
    points_count = count_points(opposite_team_score=opposite_team_score,
                                player_score=player_score,
                                player_assists=player_assists,
                                player_cards=player_cards,
                                player_minutes=player_minutes,
                                player=player)
    if points_count != 0:
        post_player_points_per_match(number_of_points=points_count,
                                     player_id=player.get('id', None),
                                     match_id=match_id)
    if player_score != 0:
        post_player_goals_per_match(number_of_goals=player_score,
                                    player_id=player.get('id', None),
                                    match_id=match_id)
