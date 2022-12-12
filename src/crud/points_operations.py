import logging
from sqlalchemy import and_
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

from src.database.session import SessionLocal
from src.models import UserPoints


session = SessionLocal()


def post_user_points_for_given_round(user_id: int, round_number: int, points_count: int) -> None:
    try:
        new_user_points = UserPoints(user_id=user_id, round=round_number, points_count=points_count)
        session.add(new_user_points)
        session.commit()
    except SQLAlchemyError as err:
        logging.error(err)
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
        logging.error(err)
        raise err
    if points is None:
        logging.error('Error Message', stack_info=True)
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
        logging.error(err)
        raise err

    if points is None:
        logging.error('Error Message', stack_info=True)
        raise ValueError(f'non existing data for given input: user_id: {user_id}')

    points_per_round_data = dict(zip(point_per_round_template, (user_id, int(points))))
    return points_per_round_data