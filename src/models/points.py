from sqlalchemy import Integer, Column, ForeignKey

from src.models import BaseClass


class Points(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    number_of_points = Column(Integer, nullable=False, unique=False, default=0)

    match_id = Column(Integer, ForeignKey('match.id'))
    player_id = Column(Integer, ForeignKey('player.id'))

    def __init__(self, number_of_points: int, match_id: int, player_id: int):
        self.number_of_points = number_of_points
        self.match_id = match_id
        self.player_id = player_id

    def __repr__(self):
        return f'[({self.id}), ({self.number_of_points}, ({self.match_id}), ({self.player_id})]'
