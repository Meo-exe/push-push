import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score



def train_model(df: pd.DataFrame):

    # One-hot encode categorical features
    encoder = OneHotEncoder(drop='first', sparse_output=False)
    encoded_features = encoder.fit_transform(df[['driver_id', 'team_id', 'race']])

    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['driver_id', 'team_id', 'race']))

    # Concatenate the encoded features with the original DataFrame
    df = pd.concat([df, encoded_df], axis=1)

    # Drop the original categorical columns
    df.drop(['driver_id', 'team_id', 'race'], axis=1, inplace=True)

    # Separate features (X) and target (y)
    y = df['finish_position']
    X = df.drop('finish_position', axis=1)

    # Encode the target variable (finish_position) as a label (1, 2, 3, etc.)
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Train a Random Forest Classifier
    model_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    model_classifier.fit(X_train, y_train)

    # Evaluate the model (optional, for debugging purposes)
    predictions_classifier = model_classifier.predict(X_test)
    y_test_decoded = label_encoder.inverse_transform(y_test)
    predictions_decoded = label_encoder.inverse_transform(predictions_classifier)
    target_names = [str(label) for label in label_encoder.classes_]

    # Return the trained model and encoders
    return model_classifier, encoder, label_encoder

def predict_next_race(model, encoder, label_encoder, race_data: pd.DataFrame):

    # One-hot encode the categorical features
    encoded_features = encoder.transform(race_data[['driver_id', 'team_id', 'race']])
    encoded_df = pd.DataFrame(
        encoded_features,
        columns=encoder.get_feature_names_out(['driver_id', 'team_id', 'race'])
    )

    # Concatenate the encoded features with the original DataFrame
    race_data = pd.concat([race_data.drop(['driver_id', 'team_id', 'race'], axis=1), encoded_df], axis=1)

    # Get prediction probabilities for each driver
    prediction_probabilities = model.predict_proba(race_data)

    # Assign unique positions based on sorted probabilities
    predicted_positions = []
    for class_index in range(prediction_probabilities.shape[1]):
        # Get probabilities for the current position
        position_probabilities = prediction_probabilities[:, class_index]

        # Sort drivers by their probabilities for this position
        sorted_indices = position_probabilities.argsort()[::-1]  
        for driver_index in sorted_indices:
            if driver_index not in predicted_positions:
                predicted_positions.append(driver_index)
                break

    # Decode the predicted positions to their original labels
    decoded_positions = label_encoder.inverse_transform(predicted_positions)

    return decoded_positions


