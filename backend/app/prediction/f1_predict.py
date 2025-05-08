from app.prediction.ds_builder import create_race_dataframe
from app.prediction.f1_model import train_model, predict_next_race
from app.database import get_db
from app.models.models import Driver, Team, Race, Result
from datetime import datetime
import pandas as pd
import schedule
import time

def get_next_race(db_session):
    """
    Find the next race for the current year that does not already exist in the results database.
    """
    # Get the current year
    current_year = datetime.now().year

    # Query all races for the current year
    races = db_session.query(Race).filter(Race.season == current_year).order_by(Race.round).all()

    # Iterate through the races and check if the race_id exists in the results database
    for race in races:
        race_exists = db_session.query(Result).filter(Result.race_id == race.race_id).first()
        if not race_exists:
            # If the race_id does not exist, return this race as the next race
            return race

    # If all races exist, return None
    return None


def predict_next():
    # Get a database session
    db_session = next(get_db())

    # Find the next race
    next_race = get_next_race(db_session)

    if not next_race:
        print("All races for the current year already exist in the results database.")
        return

    print(f"Next race identified: {next_race.name} (Race ID: {next_race.race_id})")

    # Create the training DataFrame from the database
    training_data = create_race_dataframe(db_session)

    # Train the model
    model, one_hot_encoder, label_encoder = train_model(training_data)

    # Find the previous race (the race just before the next race)
    previous_race = (
        db_session.query(Race)
        .filter(Race.season == next_race.season, Race.round < next_race.round)
        .order_by(Race.round.desc())
        .first()
    )

    if not previous_race:
        print("No previous race found. Cannot predict the next race.")
        return

    # Fetch results for the previous race
    previous_race_results = db_session.query(Result).filter(Result.race_id == previous_race.race_id).all()

    if not previous_race_results:
        print("No results found for the previous race. Cannot predict the next race.")
        return

    # Prepare the next race data
    next_race_data = pd.DataFrame({
        "driver_id": [result.driver.driver_id for result in previous_race_results],
        "team_id": [result.team.team_id for result in previous_race_results],
        "race": [next_race.name] * len(previous_race_results),
        "grid_position": [result.grid_position for result in previous_race_results],
    })

    # Predict the finish positions for the next race
    predictions = predict_next_race(model, one_hot_encoder, label_encoder, next_race_data)

    # Print the predictions
    print("Predicted finish positions for the next race:")
    for driver_id, position in zip(next_race_data['driver_id'], predictions):
        print(f"Driver {driver_id}: Predicted Position {position}")
# Schedule the prediction to run every Monday at 9:00 AM
# schedule.every().monday.at("12:00").do(predict_next)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

predict_next()


