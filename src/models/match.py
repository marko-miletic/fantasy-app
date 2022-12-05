from sqlalchemy import (
    Integer,
    Date,
    Boolean,
    Column,
    ForeignKey
)

from src.models.base import BaseClass


class Match(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, nullable=False, unique=False)
    confirmed = Column(Boolean, nullable=False, unique=False, default=True)

    home_score = Column(Integer, nullable=True, unique=False, default=None)
    away_score = Column(Integer, nullable=True, unique=False, default=None)

    home_team_id = Column(Integer, ForeignKey('country.id'))
    away_team_id = Column(Integer, ForeignKey('country.id'))

    def __init__(self, date: str, home_team_id: int, away_team_id: int):
        self.date = date
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id

    def __repr__(self):
        return f'[({self.id}), ({self.date}, ({self.home_team_id}), ({self.away_team_id})]'