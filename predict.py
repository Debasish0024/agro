import pandas as pd
import joblib
from datetime import datetime

# Load the trained model and scaler
model = joblib.load('potato_model.pkl')
scaler = joblib.load('scaler.pkl')  # Ensure this file is saved and available

def predict_potato_price(fertilizer_price, petrol_price, current_price, date, rainfall_data):
    # Convert the date into datetime object
    date = datetime.strptime(date, '%Y-%m-%d')

    # Prepare the input DataFrame with the same features as used for training
    input_data = pd.DataFrame({
        'ds': [pd.to_datetime(date)],
        'Fertilizer': [fertilizer_price],
        'Petrol Price': [petrol_price],
        'District Name': [0],  # Replace with actual district code if applicable
        'Lag_Price': [current_price],
        'Rainfall': [rainfall_data]
    })

    # Convert features to numeric
    input_data = input_data.apply(pd.to_numeric, errors='coerce')
    input_data = input_data.fillna(0)

    # Ensure the same feature order as used in training
    feature_columns = ['ds', 'Fertilizer', 'Petrol Price', 'District Name', 'Lag_Price', 'Rainfall']
    input_data = input_data.reindex(columns=feature_columns, fill_value=0)

    # Standardize features
    input_data_scaled = scaler.transform(input_data)

    # Make prediction using the model
    prediction = model.predict(input_data_scaled)

    return prediction[0]

# Example usage
fertilizer_price = 20000.0
petrol_price = 104.0
current_price = 2200.0
date = '2024-01-05'
rainfall_data = 110.0

predicted_price = predict_potato_price(fertilizer_price, petrol_price, current_price, date, rainfall_data)
print(f"Predicted Potato Price: {predicted_price:.2f} Rs./Quintal")
