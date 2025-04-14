import httpx
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.models import Driver, Team, Race, Result

async def import_f1_data(season: int, db: Session):
    """Import F1 data for a given season using the Jolpica API"""
    async with httpx.AsyncClient() as client:
        # Import drivers
        drivers_response = await client.get(f"https://api.jolpi.ca/ergast/f1/{season}/drivers.json")
        
        if drivers_response.status_code == 200:
            drivers_data = drivers_response.json()['MRData']['DriverTable']['Drivers']
            
            for driver_data in drivers_data:
                driver_id = driver_data['driverId']
                
                # Check if driver exists
                existing_driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
                
                if not existing_driver:
                    # Create new driver
                    new_driver = Driver(
                        driver_id=driver_id,
                        first_name=driver_data['givenName'],
                        last_name=driver_data['familyName'],
                        code=driver_data.get('code'),
                        number=int(driver_data['permanentNumber']) if 'permanentNumber' in driver_data else None,
                        nationality=driver_data['nationality'],
                        date_of_birth=driver_data['dateOfBirth']
                    )
                    db.add(new_driver)
        
        # Import constructors (teams)
        teams_response = await client.get(f"https://api.jolpi.ca/ergast/f1/{season}/constructors.json")
        if teams_response.status_code == 200:
            teams_data = teams_response.json()['MRData']['ConstructorTable']['Constructors']
            
            for team_data in teams_data:
                team_id = team_data['constructorId']
                
                # Check if team exists
                existing_team = db.query(Team).filter(Team.team_id == team_id).first()
                
                if not existing_team:
                    # Create new team
                    new_team = Team(
                        team_id=team_id,
                        name=team_data['name'],
                        nationality=team_data['nationality']
                    )
                    db.add(new_team)
        
        # Import races and results
        races_response = await client.get(f"https://api.jolpi.ca/ergast/f1/{season}.json")
        if races_response.status_code == 200:
            races_data = races_response.json()['MRData']['RaceTable']['Races']
            
            for race_data in races_data:
                race_id = f"{season}-{race_data['round']}"
                
                # Check if race exists
                existing_race = db.query(Race).filter(Race.race_id == race_id).first()
                
                if not existing_race:
                    # Create new race
                    new_race = Race(
                        race_id=race_id,
                        name=race_data['raceName'],
                        circuit_name=race_data['Circuit']['circuitName'],
                        country=race_data['Circuit']['Location']['country'],
                        date=race_data['date'],
                        season=season,
                        round=int(race_data['round'])
                    )
                    db.add(new_race)
                    db.flush()  # Flush to get race ID for results
                
                # Import results for this race
                results_response = await client.get(f"https://api.jolpi.ca/ergast/f1/{season}/{race_data['round']}/results.json")
                if results_response.status_code == 200:
                    results_data = results_response.json()['MRData']['RaceTable']['Races']
                    
                    if results_data:  # Check if race has results
                        for result_data in results_data[0]['Results']:
                            driver_id = result_data['Driver']['driverId']
                            team_id = result_data['Constructor']['constructorId']
                            
                            # Check if result exists
                            existing_result = db.query(Result).filter(
                                Result.race_id == race_id,
                                Result.driver_id == driver_id
                            ).first()
                            
                            if not existing_result:
                                # Create new result
                                new_result = Result(
                                    race_id=race_id,
                                    driver_id=driver_id,
                                    team_id=team_id,
                                    grid_position=int(result_data['grid']),
                                    finish_position=int(result_data['position']),
                                    points=float(result_data['points']),
                                    status=result_data['status'],
                                    fastest_lap=result_data.get('FastestLap', {}).get('rank') == "1"
                                )
                                db.add(new_result)
        
        # Commit all changes
        db.commit()
        return {"message": f"Successfully imported F1 data for {season} season"}