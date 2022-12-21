from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models.user_league import UserLeague


session = SessionLocal()


def user_in_league_check(league_id: int, user_id: int) -> bool:
    try:
        user_in_league = session.query(UserLeague)\
            .filter(and_(UserLeague.user_id == user_id, UserLeague.league_id == league_id))\
            .scalar()
        return user_in_league is not None
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err
