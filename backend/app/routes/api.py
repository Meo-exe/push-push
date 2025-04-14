from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx

from app.models.models import Driver, Team, Race, Result
from app import schemas
from app.database import get_db

router = APIRouter()

# Driver endpoints
@router.get("/drivers", response_model=List[schemas.Driver])
def get_drivers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    drivers = db.query(Driver).offset(skip).limit(limit).all()
    return drivers

@router.get("/drivers/{driver_id}", response_model=schemas.Driver)
def get_driver(driver_id: str, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

# Team endpoints
@router.get("/teams", response_model=List[schemas.Team])
def get_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = db.query(Team).offset(skip).limit(limit).all()
    return teams

@router.get("/teams/{team_id}", response_model=schemas.Team)
def get_team(team_id: str, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.team_id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# Race endpoints
@router.get("/races", response_model=List[schemas.Race])
def get_races(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    races = db.query(Race).offset(skip).limit(limit).all()
    return races

@router.get("/races/{race_id}", response_model=schemas.Race)
def get_race(race_id: str, db: Session = Depends(get_db)):
    race = db.query(Race).filter(Race.race_id == race_id).first()
    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")
    return race

# Results endpoints
@router.get("/results", response_model=List[schemas.Result])
def get_results(race_id: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(Result)
    if race_id:
        query = query.filter(Result.race_id == race_id)
    results = query.offset(skip).limit(limit).all()
    return results