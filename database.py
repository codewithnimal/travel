from sqlite3 import IntegrityError

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

#create an engine
engine = create_engine('postgresql+psycopg2://postgres:ranju123@localhost:5432/travel',echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base  =declarative_base()
