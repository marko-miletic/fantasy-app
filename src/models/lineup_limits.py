from sqlalchemy import (
    String,
    Integer,
    Column,
)

from src.models.base import BaseClass


class LineupLimits(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    gk = Column(Integer, nullable=False, unique=False)
    df = Column(Integer, nullable=False, unique=False)
    mf = Column(Integer, nullable=False, unique=False)
    fw = Column(Integer, nullable=False, unique=False)
    lineup_status = Column(String(10), nullable=False, unique=True)  # ('full' or 'active')

    def __init__(self, gk: int, df: int, mf: int, fw: int, lineup_status: str):
        self.gk = gk
        self.df = df
        self.mf = mf
        self.fw = fw
        self.lineup_status = lineup_status

    def __repr__(self):
        return f'[({self.lineup_status}), ({self.gk}, ({self.df}), ({self.mf}), ({self.fw})]'
