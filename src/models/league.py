from sqlalchemy import Integer, Boolean, Column, String, ForeignKey

from src.models import BaseClass


class League(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=False)
    current_round = Column(Integer, nullable=False, unique=False)
    active = Column(Boolean, nullable=False, unique=False, default=False)

    owner_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, name: str, owner_id: int, current_round: int = 1, active: bool = True):
        self.name = name
        self.owner_id = owner_id
        self.current_round = current_round
        self.active = active

    def __repr__(self):
        return f'[({self.id}), ({self.name}, ({self.current_round}, ({self.active})]'
