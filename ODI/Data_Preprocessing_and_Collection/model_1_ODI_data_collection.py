import os
import json
import pandas as pd

def load_and_process_data(data_dir):
    all_matches = []

    for file in os.listdir(data_dir):
        if file.endswith('.json'):
            with open(os.path.join(data_dir, file)) as f:
                match_data = json.load(f)
                
                # Check if the match_type is 'ODI' before adding to the list
                if match_data['info'].get('match_type') == 'ODI':
                    all_matches.append(match_data)

    # Parse innings data and include match type and gender
    data = []

    for match in all_matches:
        match_id = match['info']['dates'][0]
        match_type = match['info'].get('match_type', 'Unknown')
        gender = match['info'].get('gender', 'Unknown')
        city = match['info'].get('city')
        
        teams = match['info'].get('teams', [])
        if len(teams) != 2:
            continue  # Skip if the teams data is not properly structured

        # Extract winner from outcome
        winner = match['info'].get('outcome', {}).get('winner', None)

        # Process each innings
        for idx, innings in enumerate(match['innings']):
            batting_team = innings['team']
            bowling_team = teams[0] if teams[1] == batting_team else teams[1]  # Determine the bowling team

            balls = 0
            runs = 0
            wickets = 0
            cumulative_score = 0  # To store the cumulative score
            current_run_rate = 0  # To store the current run rate
            player_dismissed = 0

            # Initialize variables for second innings-specific features
            target_score = None
            runs_needed = None
            balls_left = None
            required_run_rate = None

            is_second_innings = idx == 1

            if is_second_innings:
                # Get the target score from the first innings
                target_score = data[-1]['final_score'] if data else None

            if 'overs' in innings:
                for over in innings['overs']:
                    for delivery in over['deliveries']:
                        balls += 1
                        runs += delivery['runs']['total']
                        cumulative_score += delivery['runs']['total']  # Increment cumulative score

                        # Calculate the current run rate
                        if balls > 0:
                            current_run_rate = cumulative_score / (balls / 6)  # Runs per over

                        if 'wickets' in delivery:
                            wickets += 1
                            player_dismissed += 1  # Count each wicket

                        overs_decimal = balls // 6 + (balls % 6) / 6
                        wickets_left = 10 - player_dismissed  # Calculate wickets left
                        balls_left = 300 - balls if not is_second_innings else 300 - balls
                        
                        if is_second_innings and target_score:
                            runs_needed = target_score - cumulative_score
                            required_run_rate = (runs_needed / (balls_left / 6)) if balls_left > 0 else None

                        # Add the row to the data
                        data.append({
                            'match_id': match_id,
                            'match_type': match_type,
                            'gender': gender,
                            'city': city,
                            'batting_team': batting_team,
                            'bowling_team': bowling_team,
                            'balls': balls,
                            'overs': overs_decimal,
                            'runs': cumulative_score,  # Cumulative score
                            'wickets': wickets,
                            'wickets_left': wickets_left,  # Add wickets left to the data
                            'balls_left': balls_left,  # Add balls left to the data
                            'run_rate': current_run_rate,  # Current run rate
                            'target_score': target_score,
                            'runs_needed': runs_needed,
                            'required_run_rate': required_run_rate,
                            'is_second_innings': is_second_innings,
                            'bat_first': 1 if not is_second_innings else 0,  # 1 for first innings, 0 for second
                            'winner': winner,
                            'batting_team_won': 1 if batting_team == winner else 0,  # Outcome for batting team
                            'outcome': 1 if batting_team == winner else 0,  # 1 if batting team won, 0 otherwise
                            'final_score': None
                        })

                # Assign the final score to the relevant rows
                final_score = cumulative_score
                for entry in data[-balls:]:
                    entry['final_score'] = final_score

    # Create a DataFrame from the processed data
    df = pd.DataFrame(data)
    
    # Drop records without city/venue
    df = df.dropna(subset=['city'])

    # Filter cities that appear more than 10 times
    eligible_cities = df['city'].value_counts()[df['city'].value_counts() > 10].index.tolist()
    df = df[df['city'].isin(eligible_cities)]  # Add cities that appear more than 10 times

    return df

# Path to your directory containing the JSON files
data_dir = '/Users/Harry/Documents/Harry_Hawkeye/all_json'
df = load_and_process_data(data_dir)

# Save the DataFrame to a CSV file
df.to_csv('all_odi_data.csv', index=False)
