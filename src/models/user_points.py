from sqlalchemy import Integer, Column, ForeignKey

from src.models import BaseClass


class UserPoints(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    round = Column(Integer, nullable=False, unique=False)
    points_count = Column(Integer, nullable=False, unique=False)

    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, user_id: int, round: int, points_count: int):
        self.user_id = user_id
        self.round = round
        self.points_count = points_count

    def __repr__(self):
        return f'[({self.user_id}), ({self.round}), ({self.points_count})]'
