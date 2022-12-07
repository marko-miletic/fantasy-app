from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import BaseClass
from src.models.user import User
from src.models.group import Group
from src.models.country import Country
from src.models.player import Player
from src.models.match import Match
from src.models.points import Points
from src.models.goals_scored import GoalsScored
from src.models.selected_players import SelectedPlayers
from src.models.lineup_limits import LineupLimits

# dialect+driver://username:password@host:port/database

#Session = sessionmaker(db)
#session = Session()

#BaseClass.metadata.create_all(db, checkfirst=True)
