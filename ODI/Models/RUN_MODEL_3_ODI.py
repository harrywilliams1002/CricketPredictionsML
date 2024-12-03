import pickle

# Load the model from the pickle file
model = pickle.load(open('/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/ODI/Models/MODEL_3_ODI.pkl', 'rb'))

# Example data for prediction (you should replace these with actual feature values)
new_data = {
    'balls_left': [2],  # e.g., 30 balls left
    'wickets_left': [3],  # e.g., 5 wickets left
    'run_rate': [3.75],  # e.g., current run rate of 7.5
    'runs': [180],  # e.g., 120 runs scored so far
    'batting_team': ['Ireland'],  # e.g., the batting team
    'bowling_team': ['England'],  # e.g., the bowling team
    'city': ['Melbourne'],  # e.g., the city where the match is being played
    'target_score': [280] # THIS WILL BE INPUT
}

# Convert the new data into a DataFrame
import pandas as pd
new_data_df = pd.DataFrame(new_data)

# Predict outcomes
prediction = model.predict(new_data_df)

# Predict probabilities of winning
predictions_probabilities = model.predict_proba(new_data_df)[:, 1]  # Probability of winning (positive class)

print("Predicted Outcome (0=Loss, 1=Win):", prediction[0])
print("Likelihood of Chasing Team Winning:", predictions_probabilities[0])