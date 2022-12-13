from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models import Country


session = SessionLocal()


def get_countries_count() -> int:
    try:
        countries_count = session.query(func.count(Country.id)) \
            .scalar()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err

    return countries_count
