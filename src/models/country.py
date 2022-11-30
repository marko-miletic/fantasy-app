from sqlalchemy import (
    String,
    Integer,
    Column,
    ForeignKey
)


from src.models.base import BaseClass


class Country(BaseClass):
 
    id = Column(Integer, primary_key=True, index=True)

    country = Column(String(50), nullable=False, unique=True)
    world_ranking = Column(Integer, nullable=False, unique=True)
    tournament_ranking = Column(Integer, nullable=False, unique=True)

    group_id = Column(Integer, ForeignKey('group.id'))

    def __init__(self, id: int, country: str, world_ranking: str, tournament_ranking: str, group_id: str):
        self.id = id
        self.country = country
        self.world_ranking = world_ranking
        self.tournament_ranking = tournament_ranking
        self.group_id = group_id

    def __repr__(self):
        return f'[({self.id}), ({self.country}, ({self.group_id}))]'
