import os
import json
import pandas as pd

def load_and_process_data(data_dir, teams_to_include):
    player_runs = {}  # Dictionary to store cumulative runs for each player
    player_teams = {}  # Dictionary to store the team for each player
    all_matches = []

    # Loop through JSON files in the directory
    for file in os.listdir(data_dir):
        if file.endswith('.json'):
            with open(os.path.join(data_dir, file)) as f:
                match_data = json.load(f)

                # Debugging: Print match data and check if it contains the 'ODI' type
                print(f"Processing file: {file}")
                print(f"Match type: {match_data['info'].get('match_type')}, Teams: {match_data['info'].get('teams', [])}")

                # Check if the match_type is 'ODI' and the teams are in the list
                if (
                    match_data['info'].get('match_type') == 'T20' and
                    any(team in teams_to_include for team in match_data['info'].get('teams', []))
                ):
                    all_matches.append(match_data)

    print(f"Total matches processed: {len(all_matches)}")

    # Process the matches and accumulate runs for players
    for match in all_matches:
        for innings in match['innings']:
            batting_team = innings['team']

            # Only process players for the teams in the list
            if batting_team not in teams_to_include:
                continue

            # Debugging: Print the batting team
            print(f"Processing batting team: {batting_team}")

            # Iterate over deliveries to accumulate runs per batter
            for over in innings.get('overs', []):
                for delivery in over.get('deliveries', []):
                    batter = delivery['batter']
                    batter_runs = delivery['runs']['batter']

                    # Debugging: Check batter and runs
                    print(f"Batter: {batter}, Runs scored: {batter_runs}")

                    # Accumulate runs for each batter and associate them with the batting team
                    player_runs[batter] = player_runs.get(batter, 0) + batter_runs
                    player_teams[batter] = batting_team  # Associate batter with team

    # Debugging: Show player runs and teams
    print(f"Player runs: {player_runs}")
    print(f"Player teams: {player_teams}")

    # Prepare the result for the top scorers of each team
    top_scorers_data = []
    
    # Process each team in the teams_to_include list
    for team in teams_to_include:
        # Get the players and their runs for the current team
        team_players = [(player, runs) for player, runs in player_runs.items() if player_teams.get(player) == team]
        
        # Sort the players by total runs and take the top 5
        top_scorers = sorted(team_players, key=lambda x: x[1], reverse=True)[:5]

        # Debugging: Print the top scorers for the team
        print(f"Top scorers for {team}: {top_scorers}")
        
        # Append the top scorers to the list
        for player, runs in top_scorers:
            top_scorers_data.append({
                'Team': team,
                'Player': player,
                'Total Runs': runs
            })

    # Create a DataFrame from the top scorers data
    top_scorers_df = pd.DataFrame(top_scorers_data)
    
    return top_scorers_df

# Path to your directory containing the JSON files
data_dir = '/Users/Harry/Documents/Harry_Hawkeye/all_json'

# List of teams you want to include
teams_to_include = ['India', 'Sri Lanka', 'West Indies', 'South Africa', 'Scotland', 'Bermuda', 'Mongolia', 'China', 'New Zealand', 'England', 'Australia', 'Estonia', 'Cyprus', 'Portugal', 'Spain', 'Kuwait', 'Hong Kong', 'Ireland', 'Swaziland', 'Seychelles', 'Belize', 'United States of America', 'Tanzania', 'Uganda', 'United Arab Emirates', 'Nepal', 'Thailand', 'Bangladesh', 'Norway', 'Guernsey', 'Kenya', 'Nigeria', 'Denmark', 'Italy', 'Netherlands', 'Finland', 'Sweden', 'Maldives', 'Japan', 'Vanuatu', 'Bahrain', 'Namibia', 'Croatia', 'Zimbabwe', 'Pakistan', 'Malaysia', 'Romania', 'Czech Republic', 'ICC World XI', 'Indonesia', 'Philippines', 'Gibraltar', 'Rwanda', 'Singapore', 'Oman', 'Bulgaria', 'Malta', 'Switzerland', 'Myanmar', 'Serbia', 'Bhutan', 'Cook Islands', 'Austria', 'Germany', 'Samoa', 'Eswatini', 'Brazil', 'Ghana', 'Qatar', 'Mozambique', 'Lesotho', 'Belgium', 'Bahamas', 'Argentina', 'Sierra Leone', 'France', 'Cameroon', 'Malawi', 'Jersey', 'Panama', 'Hungary', 'Isle of Man', 'Gambia', 'Papua New Guinea', 'Canada', 'Mexico', 'Costa Rica', 'Luxembourg', 'Fiji', 'Botswana', 'Greece', 'Cayman Islands', 'Saudi Arabia', 'South Korea', 'St Helena', 'Cambodia', 'Mali', 'Israel', 'Barbados', 'Slovenia', 'Turkey', 'Iran']
# Load the data and get top scorers for the specified teams
top_scorers_df = load_and_process_data(data_dir, teams_to_include)

# Save the top scorers for each team to a CSV file
top_scorers_df.to_csv('top_five_scorers_per_team_T20.csv', index=False)