import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import math
import joblib

def convert_to_classes(probability):
    return math.ceil(7 * probability)

def train_model():
# Load the data
    data = pd.read_csv("flood_2.csv")

    # Apply the function to the FloodProbability column to create a new 'FloodRiskClass' column
    data['FloodRiskClass'] = data['FloodProbability'].apply(convert_to_classes)

    # Define the features (all columns except 'FloodProbability' and 'FloodRiskClass')
    X = data.drop(columns=['FloodProbability', 'FloodRiskClass'])
    y = data['FloodRiskClass']

    # Split the dataset into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier()

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print(classification_report(y_test, y_pred))

    # Save the trained model to a file
    joblib.dump(model, 'flood_risk_model.pkl')

    # Predict on new property data
    new_property = [[4,4,3,4,0.4,6,8,8]]  # Sample new property data
    predicted_risk = model.predict(new_property)
    print("Predicted Flood Risk (1 to 7 scale):", predicted_risk[0])

def predict_flood_value(value):
    # Load the trained model from the file
    model = joblib.load('flood_risk_model.pkl')

    # Predict on new property data
    # value = {
    #     'max_rain': np.float32(11.1), 
    #     'avg_rain': np.float32(0.123512715), 
    #     'avg_soil_moisture': np.float32(0.24416439), 
    #     'avg_water_prox': np.float32(9.376547), 
    #     'precipitation': np.float32(3.7458448), 
    #     'elevation': 9.0, 
    #     'population': 5.0,
    #     'FEMA prediction': '2.97'
    # }

    # Round the necessary numerical values (rounded to 2 decimal places)
    value_cleaned = {
        'max_rain': round(float(value['max_rain']), 2), 
        'avg_rain': round(float(value['avg_rain']), 2), 
        'avg_soil_moisture': round(float(value['avg_soil_moisture']), 2), 
        'avg_water_prox': round(float(value['avg_water_prox']), 2), 
        'precipitation': round(float(value['precipitation']), 2), 
        'elevation': round(float(value['elevation']), 2), 
        'population': round(float(value['population']), 2)
    }
    
    # max_rain	Elevation	precipitation	Encroachments	Avg_soil_moisture	Avg_water_prox	DeterioratingInfrastructure	PopulationScore	FloodProbability


    new_property = [[
        value_cleaned['max_rain'],
        value_cleaned['elevation'],
        value_cleaned["precipitation"],
        value_cleaned["avg_rain"],
        value_cleaned["avg_soil_moisture"],
        value_cleaned["avg_water_prox"],
        4,  # Assuming the 4 is a constant as in the original example
        value_cleaned["population"]
    ]]
    predicted_risk = model.predict(new_property)
    print("Predicted Flood Risk (1 to 7 scale):", predicted_risk[0])
    
    result = {
        "predicted_value": int(predicted_risk[0]),  # Convert np.int64 to int
        "max_rain": round(float(value['max_rain']), 2),
        "avg_rain": round(float(value['avg_rain']), 2),
        "avg_soil_moisture": round(float(value['avg_soil_moisture']), 2),
        "avg_water_prox": round(float(value['avg_water_prox']), 2),
        "precipitation": round(float(value['precipitation']), 2),
        "elevation": round(float(value['elevation']), 2),
        "population": int(value['population']),  # Convert np.int64 to int
        "FEMA prediction": str(value['FEMA prediction'])  # Ensure it's a string
    }
    return result

