import pickle

# Load the model from the pickle file
model = pickle.load(open('/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/ODI/Models/MODEL_1_ODI.pkl', 'rb'))

# Example data for prediction (you should replace these with actual feature values)
new_data = {
    'balls_left': [12],  # e.g., 30 balls left
    'wickets_left': [4],  # e.g., 5 wickets left
    'run_rate': [5],  # e.g., current run rate of 7.5
    'runs': [240],  # e.g., 120 runs scored so far
    'batting_team': ['Ireland'],  # e.g., the batting team
    'bowling_team': ['England'],  # e.g., the bowling team
    'city': ['Melbourne']  # e.g., the city where the match is being played
}

# Convert the new data into a DataFrame
import pandas as pd
new_data_df = pd.DataFrame(new_data)

# Use the loaded model to make predictions
predictions = model.predict(new_data_df)

print("Predicted final score:", predictions)
