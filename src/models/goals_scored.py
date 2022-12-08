from sqlalchemy import Integer, Column, ForeignKey

from src.models import BaseClass


class GoalsScored(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    number_of_goals = Column(Integer, nullable=False, unique=False)

    match_id = Column(Integer, ForeignKey('match.id'))
    player_id = Column(Integer, ForeignKey('player.id'))

    def __init__(self, number_of_goals: int, match_id: int, player_id: int):
        self.number_of_goals = number_of_goals
        self.match_id = match_id
        self.player_id = player_id

    def __repr__(self):
        return f'[({self.id}), ({self.date}, ({self.home_team}), ({self.away_team})]'
