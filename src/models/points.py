from sqlalchemy import Integer, Column, ForeignKey

from src.models import BaseClass


class Points(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    number_of_points = Column(Integer, nullable=False, unique=False, default=0)

    match_id = Column(Integer, ForeignKey('match.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, number_of_points: int, match_id: int, user_id: int):
        self.number_of_points = number_of_points
        self.match_id = match_id
        self.user_id = user_id

    def __repr__(self):
        return f'[({self.id}), ({self.date}, ({self.home_team_id}), ({self.away_team_id})]'
