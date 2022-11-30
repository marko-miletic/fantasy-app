from flask_login import UserMixin

from sqlalchemy import String, Integer, Column

from src.models.base import BaseClass


class User(UserMixin, BaseClass):
    """
        roles:
        0 - user
        1 - content moderator
        2 - admin
    """
 
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False, unique=False)
    
    role = Column(Integer, nullable=False, unique=False)

    def __init__(self, name: str, email: str, password: str, role: int = 0):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        role_values = {
            0: 'user',
            1: 'content manager',
            2: 'admin'
        }
        return f'[({self.name}), ({self.email}), ({role_values[self.role]})]'
