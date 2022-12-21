from sqlalchemy import and_
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models import UserPoints, Points, GoalsScored, Player, SelectedPlayers


session = SessionLocal()


def post_user_points_for_given_round(user_id: int, round_number: int, points_count: int) -> None:
    try:
        new_user_points = UserPoints(user_id=user_id, round=round_number, points_count=points_count)
        session.add(new_user_points)
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err


def get_points_per_user_per_round(user_id: int, round_number: int) -> dict:
    point_per_round_template = [
        'user',
        'round',
        'points'
    ]

    try:
        points = session.query(UserPoints.points_count)\
            .filter(and_(UserPoints.user_id == user_id, UserPoints.round == round_number))\
            .scalar()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err
    if points is None:
        logger.logging.error('Error Message', stack_info=True)
        raise ValueError(f'non existing data for given input: user_id: {user_id}, round: {round_number}')

    points_per_round_data = dict(zip(point_per_round_template, (user_id, round_number, int(points))))
    return points_per_round_data


def get_points_per_user(user_id: int) -> dict:
    point_per_round_template = [
        'user',
        'points'
    ]

    try:
        points = session.query(func.sum(UserPoints.points_count))\
            .filter(UserPoints.user_id == user_id)\
            .scalar()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    if points is None:
        logger.logging.error('Error Message', stack_info=True)
        raise ValueError(f'non existing data for given input: user_id: {user_id}')

    points_per_round_data = dict(zip(point_per_round_template, (user_id, int(points))))
    return points_per_round_data


def post_player_points_per_match(number_of_points: int, player_id: int, match_id: int) -> None:
    try:
        new_player_points = Points(number_of_points=number_of_points, player_id=player_id, match_id=match_id)
        session.add(new_player_points)
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err


def post_player_goals_per_match(number_of_goals: int, player_id: int, match_id: int) -> None:
    try:
        new_player_points = GoalsScored(number_of_goals=number_of_goals, player_id=player_id, match_id=match_id)
        session.add(new_player_points)
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err


def get_sum_user_round_points(user_id: int, round_number: int):
    try:
        points = session.query(func.sum(Points.number_of_points))\
            .join(Player).join(SelectedPlayers).join(UserPoints)\
            .filter(and_(SelectedPlayers.active == True,
                         UserPoints.round == round_number,
                         UserPoints.user_id == user_id))\
            .scalar()
        return points
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err
