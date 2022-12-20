from sqlalchemy import and_, desc
from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.crud.match_operations import get_matches_by_status


session = SessionLocal()


def get_active_matches() -> list:
    return get_matches_by_status(status='active')


