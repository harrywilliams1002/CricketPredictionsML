from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Load models
models = {
    'ODI_model_1': pickle.load(open('/Users/harry/Documents/Harry_Hawkeye/New_double_innings_approach/Flask_App/models/MODEL_1_ODI.pkl', 'rb')),
    'ODI_model_2': pickle.load(open('/Users/harry/Documents/Harry_Hawkeye/New_double_innings_approach/Flask_App/models/MODEL_2_ODI.pkl', 'rb')),
    'ODI_model_3': pickle.load(open('/Users/harry/Documents/Harry_Hawkeye/New_double_innings_approach/Flask_App/models/MODEL_3_ODI.pkl', 'rb')),
    
    'T20_model_1': pickle.load(open('/Users/harry/Documents/Harry_Hawkeye/New_double_innings_approach/Flask_App/models/MODEL_1_T20.pkl', 'rb')),
    'T20_model_2': pickle.load(open('/Users/harry/Documents/Harry_Hawkeye/New_double_innings_approach/Flask_App/models/MODEL_2_T20.pkl', 'rb')),
    'T20_model_3': pickle.load(open('/Users/harry/Documents/Harry_Hawkeye/New_double_innings_approach/Flask_App/models/MODEL_3_T20.pkl', 'rb')),
}

# Route to render the initial form
@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Handle JSON request data
    match_type = data.get('match_type')
    innings_choice = data.get('innings_choice')
    balls_left = int(data.get('balls_left', 0))
    wickets_left = int(data.get('wickets_left', 0))
    runs = int(data.get('runs', 0))
    run_rate = float(data.get('run_rate', 0.0))
    city = data.get('city')
    batting_team = data.get('batting_team')
    bowling_team = data.get('bowling_team')
    target_score = int(data.get('target_score', 0)) if data.get('target_score') else None

    # Select the correct models based on match type and innings choice
    try:
        if match_type == 'ODI' and innings_choice == 'batting_first':
            model_1 = models['ODI_model_1']
            model_2 = models['ODI_model_2']
        elif match_type == 'ODI' and innings_choice == 'chasing':
            model_3 = models['ODI_model_3']
        elif match_type == 'T20' and innings_choice == 'batting_first':
            model_1 = models['T20_model_1']
            model_2 = models['T20_model_2']
        elif match_type == 'T20' and innings_choice == 'chasing':
            model_3 = models['T20_model_3']
        else:
            return jsonify({'error': 'Invalid input'}), 400
    except KeyError:
        return jsonify({'error': 'Model loading error'}), 500

    # Prepare input features
    batting_first_features = {
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'runs': [runs],
        'run_rate': [run_rate],
        'city': [city],
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
    }

    chasing_features = {
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'runs': [runs],
        'run_rate': [run_rate],
        'city': [city],
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'target_score': [target_score],
    }

    # Convert features to DataFrame
    batting_first_input_df = pd.DataFrame(batting_first_features)
    chasing_input_df = pd.DataFrame(chasing_features)

    # Model-specific logic
    result = {}
    if match_type == 'ODI' and innings_choice == 'batting_first':
        # Predict final score using model_1
        final_score_1 = model_1.predict(batting_first_input_df)[0]
        batting_first_input_df['final_score'] = final_score_1  # Add predicted final_score for model_2

        # Predict outcome and probability using model_2
        y_pred_2 = model_2.predict(batting_first_input_df)[0]
        y_pred_proba_2 = model_2.predict_proba(batting_first_input_df)[:, 1][0]

        result = {
            'predicted_score': int(final_score_1),
            'predicted_outcome': 'Win' if y_pred_2 == 1 else 'Lose',
            'win_probability': round(y_pred_proba_2 * 100, 2)
        }

    elif match_type == 'ODI' and innings_choice == 'chasing':
                # Predict outcome and probability using model_3
        y_pred_3 = model_3.predict(chasing_input_df)[0]
        y_pred_proba_3 = model_3.predict_proba(chasing_input_df)[:, 1][0]

        balls_left = chasing_input_df['balls_left'].iloc[0]
        runs = chasing_input_df['runs'].iloc[0]
        target_score = chasing_input_df['target_score'].iloc[0]

        # Calculate runs needed
        runs_needed = target_score - runs

        # Adjust probabilities based on cricket constraints
        if balls_left * 6 < runs_needed:
        # Not enough balls to achieve the target
            adjusted_win_probability = 0
            predicted_outcome = 'Lose'
        else:
            # Use model's predicted probability
            adjusted_win_probability = round(y_pred_proba_3 * 100, 2)
            predicted_outcome = 'Win' if y_pred_3 == 1 else 'Lose'

        result = {
            'predicted_score': None,
            'predicted_outcome': predicted_outcome,
            'win_probability': adjusted_win_probability
        }

    elif match_type == 'T20' and innings_choice == 'batting_first':
        # Predict final score using model_1
        final_score_1 = model_1.predict(batting_first_input_df)[0]
        batting_first_input_df['final_score'] = final_score_1  # Add predicted final_score for model_2

        # Predict outcome and probability using model_2
        y_pred_2 = model_2.predict(batting_first_input_df)[0]
        y_pred_proba_2 = model_2.predict_proba(batting_first_input_df)[:, 1][0]

        result = {
            'predicted_score': int(final_score_1),
            'predicted_outcome': 'Win' if y_pred_2 == 1 else 'Lose',
            'win_probability': round(y_pred_proba_2 * 100, 2)
        }

    elif match_type == 'T20' and innings_choice == 'chasing':
        # Predict outcome and probability using model_3
        y_pred_3 = model_3.predict(chasing_input_df)[0]
        y_pred_proba_3 = model_3.predict_proba(chasing_input_df)[:, 1][0]

        balls_left = chasing_input_df['balls_left'].iloc[0]
        runs = chasing_input_df['runs'].iloc[0]
        target_score = chasing_input_df['target_score'].iloc[0]

        # Calculate runs needed
        runs_needed = target_score - runs

        # Adjust probabilities based on cricket constraints
        if balls_left * 6 < runs_needed:
        # Not enough balls to achieve the target
            adjusted_win_probability = 0
            predicted_outcome = 'Lose'
        else:
            # Use model's predicted probability
            adjusted_win_probability = round(y_pred_proba_3 * 100, 2)
            predicted_outcome = 'Win' if y_pred_3 == 1 else 'Lose'


        result = {
            'predicted_score': None,
            'predicted_outcome': predicted_outcome,
            'win_probability': adjusted_win_probability
        }

    else:
        return jsonify({'error': 'Invalid input'}), 400

    # Return result
    return jsonify(result)

@app.route('/top_scorers', methods=['POST'])
def top_scorers():
    # Extract match type, batting team, and bowling team from the request
    data = request.json
    match_type = data.get('match_type')  # This will be either 'ODI' or 'T20'
    team1 = data.get('batting_team')
    team2 = data.get('bowling_team')

    # Debug: Print incoming request data
    print("Received data:", data)

    # Validate that match_type is valid (either ODI or T20)
    if match_type not in ['ODI', 'T20']:
        print("Invalid match type:", match_type)  # Debugging invalid match_type
        return jsonify({'error': 'Invalid match type. It must be either "ODI" or "T20".'}), 400
    
    # Define the path to the CSV file dynamically based on the match type
    csv_file = f'/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/Scorers/{match_type}_top_scorers.csv'
    print("Reading CSV file:", csv_file)  # Debugging: print file path

    # Attempt to read the CSV file
    try:
        df = pd.read_csv(csv_file)
        print("CSV loaded successfully:", df.head())  # Debugging: print top rows of the dataframe
    except FileNotFoundError:
        print("File not found:", csv_file)  # Debugging: print error if file is not found
        return jsonify({'error': f"File {csv_file} not found."}), 404

    # Filter the data for the selected teams (top 5 players)
    team1_data = df[df['Team'] == team1].head(5).to_dict(orient='records')
    team2_data = df[df['Team'] == team2].head(5).to_dict(orient='records')

    # Debug: Print the data being returned for both teams
    print(f"Top scorers for {team1}: {team1_data}")
    print(f"Top scorers for {team2}: {team2_data}")

    # Return the data as JSON response
    return jsonify({'team1': team1_data, 'team2': team2_data})

@app.route('/top_ratios', methods=['POST'])
def top_ratios():
    # Extract match type, batting team, and bowling team from the request
    data = request.json
    match_type = data.get('match_type')  # This will be either 'ODI' or 'T20'
    team1 = data.get('batting_team')
    team2 = data.get('bowling_team')

    # Debug: Print incoming request data
    print("Received data:", data)

    # Validate that match_type is valid (either ODI or T20)
    if match_type not in ['ODI', 'T20']:
        print("Invalid match type:", match_type)  # Debugging invalid match_type
        return jsonify({'error': 'Invalid match type. It must be either "ODI" or "T20".'}), 400
    
    # Define the path to the CSV file dynamically based on the match type
    # Assuming the CSV file contains a 'Ratio' column for the players
    csv_file = f'/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/PlayerRatios/top_5_player_win_ratios_{match_type}.csv'
    print("Reading CSV file:", csv_file)  # Debugging: print file path

    # Attempt to read the CSV file
    try:
        df = pd.read_csv(csv_file)
        print("CSV loaded successfully:", df.head())  # Debugging: print top rows of the dataframe
    except FileNotFoundError:
        print("File not found:", csv_file)  # Debugging: print error if file is not found
        return jsonify({'error': f"File {csv_file} not found."}), 404

    # Assuming that 'Player' and 'Ratio' columns exist, and 'Team' to filter by teams
    # Sort the data by the 'Ratio' column in descending order and pick top 5
    team1_data = df[df['Team'] == team1].nlargest(5, 'Ratio').to_dict(orient='records')
    team2_data = df[df['Team'] == team2].nlargest(5, 'Ratio').to_dict(orient='records')

    # Debug: Print the data being returned for both teams
    print(f"Top ratios for {team1}: {team1_data}")
    print(f"Top ratios for {team2}: {team2_data}")

    # Return the data as JSON response
    return jsonify({'team1': team1_data, 'team2': team2_data})



if __name__ == '__main__':
    app.run(debug=True)
