from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import BaseClass
from .user import User
from .group import Group
from .country import Country
from .player import Player
from .match import Match
from .points import Points
from .goals_scored import GoalsScored
from .selected_players import SelectedPlayers
from .lineup_limits import LineupLimits

# dialect+driver://username:password@host:port/database

# Session = sessionmaker(db)
# session = Session()

# BaseClass.metadata.create_all(db, checkfirst=True)
