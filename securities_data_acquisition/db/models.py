# pyright: reportMissingImports=false
from pathlib import Path
import sys
project_root = Path(__file__).parents[2].resolve()
sys.path.insert(0, str(project_root))

from sqlalchemy import Column, Float, Integer, String, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, Time

from securities_data_acquisition.db.common import Base, db_engine


class Country(Base):
    __tablename__ = "country"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer,primary_key=True)
    name = Column(String(50), nullable=False)
    slug = Column(String(5), nullable=False)

    securities_exchanges = relationship("SecuritiesExchange", back_populates="country")

    def __repr__(self) -> str:
        return super().__repr__()


class SecuritiesExchange(Base):
    __tablename__ = "securities_exchange"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer,primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    country_id = Column(ForeignKey("country.id"), nullable=False)
    profile = Column(String)

    country = relationship("Country", back_populates="securities_exchanges")
    companies = relationship("Company", back_populates="securities_exchange")


class Company(Base):
    __tablename__ = "company"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer,primary_key=True)
    name = Column(String, nullable=False, index=True)
    ticker_symbol = Column(String(10), nullable=False, index=True)
    securities_exchange_id = Column(ForeignKey("securities_exchange.id"), nullable=False)
    profile = Column(String)

    securities_exchange = relationship("SecuritiesExchange", back_populates="companies")
    historical_stock = relationship("HistoricalStockData", back_populates="company")
    # live_stock = relationship("LiveStockData", back_populates="company")


class HistoricalStockData(Base):
    __tablename__ = "historical_stock_data"
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger,primary_key=True)
    company_id = Column(ForeignKey("company.id"), nullable=False)
    date = Column(Date, nullable=False)
    high_price = Column(Float(precision=2), nullable=True)
    low_price = Column(Float(precision=2), nullable=True)
    closing_price = Column(Float(precision=2), nullable=False)
    turnover = Column(Float(precision=2), nullable=True)
    volume = Column(Float(precision=2), nullable=True)

    company = relationship("Company", back_populates="historical_stock")


class LiveStockData(Base):
    __tablename__ = "live_stock_data"
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger,primary_key=True)
    company = Column(String, nullable=False)
    # company = Column(ForeignKey("company.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    price = Column(Float(precision=2), nullable=True)

    # company = relationship("Company", back_populates="live_stock")


def create_tables():
    Base.metadata.create_all(db_engine)

if __name__ == "__main__":
    create_tables()