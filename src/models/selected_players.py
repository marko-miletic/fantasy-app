from sqlalchemy import (
    Integer,
    Boolean,
    Column,
    ForeignKey
)

from src.models.base import BaseClass


class SelectedPlayers(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    active = Column(Boolean, nullable=False, unique=False, default=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    player_id = Column(Integer, ForeignKey('player.id'))

    def __init__(self, user_id: int, player_id: int):
        self.user_id = user_id
        self.player_id = player_id

    def __repr__(self):
        return f'[({self.user_id}), ({self.player_id}), ({self.active})]'
