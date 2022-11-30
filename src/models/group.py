from sqlalchemy import String, Integer, Column

from src.models.base import BaseClass


class Group(BaseClass):
    
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(1), nullable=False, unique=True)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'[({self.id}), ({self.name})]'
