from sqlalchemy import Integer, Column, ForeignKey, Boolean

from src.models import BaseClass


class UserLeague(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    approved_access = Column(Boolean, nullable=False, unique=False, default=False)
    points = Column(Integer, nullable=False, unique=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    league_id = Column(Integer, ForeignKey('league.id'))

    def __init__(self, user_id: int, league_id: int, points: int = 0):
        self.points = points
        self.user_id = user_id
        self.league_id = league_id

    def __repr__(self):
        return f'[({self.user_id}), ({self.league_id}, ({self.points}), ({self.approved_access})]'
