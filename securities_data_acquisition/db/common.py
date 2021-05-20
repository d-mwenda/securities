from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

connection_string = "postgresql+psycopg2://securities_dba:Data_1s_fr33@localhost/securities"

db_engine = create_engine(connection_string, future=True, echo=True)

Session = sessionmaker(bind=db_engine)

Base = declarative_base()
