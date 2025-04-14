from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

# Driver schemas
class DriverBase(BaseModel):
    driver_id: str
    first_name: str
    last_name: str
    code: Optional[str] = None
    number: Optional[int] = None
    nationality: Optional[str] = None
    date_of_birth: Optional[date] = None

class DriverCreate(DriverBase):
    pass

class Driver(DriverBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Team schemas
class TeamBase(BaseModel):
    team_id: str
    name: str
    nationality: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Race schemas
class RaceBase(BaseModel):
    race_id: str
    name: str
    circuit_name: str
    country: Optional[str] = None
    date: date
    season: int
    round: int

class RaceCreate(RaceBase):
    pass

class Race(RaceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Result schemas
class ResultBase(BaseModel):
    race_id: str
    driver_id: str
    team_id: str
    grid_position: Optional[int] = None
    finish_position: Optional[int] = None
    points: Optional[float] = None
    status: Optional[str] = None
    fastest_lap: Optional[bool] = False

class ResultCreate(ResultBase):
    pass

class Result(ResultBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True