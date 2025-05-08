import pandas as pd
from sqlalchemy.orm import Session, joinedload
from app.models.models import Driver, Team, Race, Result
from app.database import get_db


def create_race_dataframe(db: Session):
    """
    Create a DataFrame from the database containing race data and save it as a CSV file.
    """
    # Query the database and construct the DataFrame
    results = db.query(Result).options(
        joinedload(Result.driver),
        joinedload(Result.team),
        joinedload(Result.race)
    ).all()
    # Align data based on relationships
    data = {
        "driver_id": [result.driver.driver_id for result in results],
        "team_id": [result.team.team_id for result in results],
        "race": [result.race.name for result in results],  # Assuming Result has a relationship to Race
        "grid_position": [result.grid_position for result in results],
        "finish_position": [result.finish_position for result in results],
    }
    # print("Data:", data)  # Debugging line to check the data structure
    
    df = pd.DataFrame(data)

    return df





