from sqlalchemy import (
    String,
    Integer,
    Date,
    Column,
    ForeignKey
)


from src.models.base import BaseClass


class Player(BaseClass):
 
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False, unique=False)
    number = Column(Integer, nullable=False, unique=False)
    position = Column(String, nullable=False, unique=False)
    birth_date = Column(Date, nullable=False, unique=False)

    country_id = Column(Integer, ForeignKey('country.id'))

    def __init__(self, id: int, name: str, number: int, position: str, birth_date: Date, country_id: int):
        self.id = id
        self.name = name
        self.number = number
        self.position = position
        self.birth_date = birth_date
        self.country_id = country_id

    def __repr__(self):
        return f'[({self.id}), ({self.name}, ({self.number}), ({self.position})]'
