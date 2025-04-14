from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    code = Column(String(3))
    number = Column(Integer)
    nationality = Column(String)
    date_of_birth = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    nationality = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

class Race(Base):
    __tablename__ = "races"
    
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    circuit_name = Column(String, nullable=False)
    country = Column(String)
    date = Column(Date, nullable=False)
    season = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

class Result(Base):
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(String, ForeignKey("races.race_id"))
    driver_id = Column(String, ForeignKey("drivers.driver_id"))
    team_id = Column(String, ForeignKey("teams.team_id"))
    grid_position = Column(Integer)
    finish_position = Column(Integer)
    points = Column(Float)
    status = Column(String)
    fastest_lap = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())