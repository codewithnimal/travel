from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)

class Destination(Base):
    __tablename__ = 'destinations'
    id = Column(Integer, primary_key=True,index=True)
    name=Column(String)
    city = Column(String)
    category = Column(String)
    rating = Column(Float)

class Favourites(Base):
    __tablename__ = 'favourites'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    destination_id = Column(Integer, ForeignKey('destinations.id'))

