from sqlalchemy import or_

from src.database.session import SessionLocal
from src.models import Match, Country
from sqlalchemy.orm import aliased


session = SessionLocal()


def get_matches_by_status(status: int = 0) -> list:
    match_status_switch = {
        0: or_(Match.confirmed == True, Match.confirmed == False),  # all matches
        1: Match.confirmed == True,  # finished matches
        -1: Match.confirmed == False  # active_matches
    }

    matches_template = [
        'date',
        'home_team_id',
        'home_team',
        'away_team_id',
        'away_team',
        'home_team_score',
        'away_team_score',
        'confirmed'
    ]

    home_country = aliased(Country)
    away_country = aliased(Country)
    matches = session.query(
        Match.date,
        Match.home_team_id,
        home_country.country,
        Match.away_team_id,
        away_country.country,
        Match.home_score,
        Match.away_score,
        Match.confirmed
    )\
        .join(home_country, home_country.id == Match.home_team_id)\
        .join(away_country, away_country.id == Match.away_team_id)\
        .filter(match_status_switch[status]).all()

    matches_data = [dict(zip(matches_template, tuple(row))) for row in matches]
    return matches_data


def post_create_new_match(date: str, home_team_id: int, away_team_id):
    new_match = Match(date=date, home_team_id=home_team_id, away_team_id=away_team_id)

    session.add(new_match)
    session.commit()


def update_change_match_status(match_id: int, new_status: bool = True):
    session.query(Match).filter(Match.id == match_id).update({Match.confirmed: new_status})
    session.commit()
