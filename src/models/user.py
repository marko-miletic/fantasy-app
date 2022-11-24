from flask_login import UserMixin

from sqlalchemy import String, Integer, Column

from src.models.base import BaseClass


class User(UserMixin, BaseClass):
 
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False, unique=False)

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'[({self.name}), ({self.email})]'
