import pickle
import pandas as pd

# Load the model from the pickle file
model = pickle.load(open('/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/ODI/Models/MODEL_2_ODI.pkl', 'rb'))

# Example data for prediction (you should replace these with actual feature values)
new_data = {
    'batting_team': ['Ireland'],  # e.g., the batting team
    'bowling_team': ['England'],  # e.g., the bowling team
    'city': ['Melbourne'],  # e.g., the city where the match is being played
    'final_score': [288.90686]  # THIS IS TAKEN FROM RESULT OF MODEL 1 !!!!!!!!
}

# Convert the new data into a DataFrame
new_data_df = pd.DataFrame(new_data)

# Ensure the data matches the format expected by the model (e.g., numeric columns, correct categories)
new_data_df['final_score'] = pd.to_numeric(new_data_df['final_score'])  # Convert to numeric if needed

# Use the loaded model to make predictions
predicted_outcome = model.predict(new_data_df)  # Predicted outcome (1 for win, 0 for loss)
predicted_probabilities = model.predict_proba(new_data_df)[:, 1]  # Probability of batting team winning

# Display the results
print("Predicted Outcome (0=Loss, 1=Win):", predicted_outcome[0])
print("Likelihood of Batting Team Winning:", predicted_probabilities[0])

