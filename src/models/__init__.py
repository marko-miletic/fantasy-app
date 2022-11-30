from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import BaseClass
from src.models.user import User
from src.models.group import Group
from src.models.country import Country
from src.models.player import Player


# dialect+driver://username:password@host:port/database

#Session = sessionmaker(db)
#session = Session()

#BaseClass.metadata.create_all(db, checkfirst=True)
