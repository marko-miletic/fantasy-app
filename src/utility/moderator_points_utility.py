from src.crud.points_operations import post_player_goals_per_match, post_player_points_per_match


def count_points(oposite_team_score: int, player_score: int, player: dict) -> int:
    points_count = 3 * player_score
    if player.get('position', None) == 'DF' and oposite_team_score == 0:
        points_count += 3
    return points_count


def define_player_points_and_goals_per_match(oposite_team_score: int,
                                             player_score: int,
                                             player: dict,
                                             match_id: int):
    points_count = count_points(oposite_team_score=oposite_team_score,
                                player_score=player_score,
                                player=player)
    post_player_points_per_match(number_of_points=points_count,
                                 player_id=player.get('id', None),
                                 match_id=match_id)
    post_player_goals_per_match(number_of_goals=player_score,
                                player_id=player.get('id', None),
                                match_id=match_id)


