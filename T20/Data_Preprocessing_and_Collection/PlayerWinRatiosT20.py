import os
import json
import pandas as pd

def calculate_player_win_ratios(data_dir, teams_to_include):
    player_stats = {}
    team_stats = {}

    # Process all match files in the directory
    for file in os.listdir(data_dir):
        if file.endswith('.json'):
            with open(os.path.join(data_dir, file)) as f:
                match_data = json.load(f)
                info = match_data.get('info', {})
                teams = info.get('players', {})
                outcome = info.get('outcome', {})
                winner = outcome.get('winner')

                # Record match results and player appearances only for specified teams
                for team, players in teams.items():
                    if team not in teams_to_include:
                        continue

                    if team not in team_stats:
                        team_stats[team] = {'matches_played': 0, 'matches_won': 0}
                    team_stats[team]['matches_played'] += 1
                    if winner == team:
                        team_stats[team]['matches_won'] += 1

                    for player in players:
                        if player not in player_stats:
                            player_stats[player] = {
                                'team': team,
                                'matches_played_with_team': 0,
                                'matches_won_with_team': 0,
                                'matches_played_total': 0,
                                'matches_won_total': 0
                            }
                        player_stats[player]['matches_played_with_team'] += 1
                        if winner == team:
                            player_stats[player]['matches_won_with_team'] += 1

    # Calculate win totals excluding the player's participation
    for player, stats in player_stats.items():
        total_matches = sum(t['matches_played'] for t in team_stats.values())
        total_wins = sum(t['matches_won'] for t in team_stats.values())
        stats['matches_played_total'] = total_matches - stats['matches_played_with_team']
        stats['matches_won_total'] = total_wins - stats['matches_won_with_team']

    # Compile win ratios for each player
    win_ratios = []
    for player, stats in player_stats.items():
        total_games_played = stats['matches_played_with_team'] + stats['matches_played_total']
        if stats['matches_played_with_team'] >= 10 and total_games_played >= 30:  # Filter for 30+ matches
            win_with = stats['matches_won_with_team'] / max(stats['matches_played_with_team'], 1)
            win_without = stats['matches_won_total'] / max(stats['matches_played_total'], 1)
            win_ratios.append({
                'Player': player,
                'Team': stats['team'],
                'Win Percentage With Team': round(win_with * 100, 2),
                'Games Played With Team': stats['matches_played_with_team'],
                'Win Percentage Without Team': round(win_without * 100, 2),
                'Games Played Without Team': stats['matches_played_total'],
                'Ratio': round(win_with / max(win_without, 0.01), 2)
            })

    # Convert to DataFrame and group by Team
    df = pd.DataFrame(win_ratios)
    top_5_per_team = (
        df.sort_values(['Team', 'Ratio'], ascending=[True, False])
          .groupby('Team')
          .head(5)
    )

    return top_5_per_team

# Directory containing the match JSON files
data_dir = '/Users/Harry/Documents/Harry_Hawkeye/t20s_json'

# List of teams to include
teams_to_include = ['India', 'Sri Lanka', 'West Indies', 'South Africa', 'Scotland', 'Bermuda', 'Mongolia', 'China', 'New Zealand', 'England', 'Australia', 'Estonia', 'Cyprus', 'Portugal', 'Spain', 'Kuwait', 'Hong Kong', 'Ireland', 'Swaziland', 'Seychelles', 'Belize', 'United States of America', 'Tanzania', 'Uganda', 'United Arab Emirates', 'Nepal', 'Thailand', 'Bangladesh', 'Norway', 'Guernsey', 'Kenya', 'Nigeria', 'Denmark', 'Italy', 'Netherlands', 'Finland', 'Sweden', 'Maldives', 'Japan', 'Vanuatu', 'Bahrain', 'Namibia', 'Croatia', 'Zimbabwe', 'Pakistan', 'Malaysia', 'Romania', 'Czech Republic','Indonesia', 'Philippines', 'Gibraltar', 'Rwanda', 'Singapore', 'Oman', 'Bulgaria', 'Malta', 'Switzerland', 'Myanmar', 'Serbia', 'Bhutan', 'Cook Islands', 'Austria', 'Germany', 'Samoa', 'Eswatini', 'Brazil', 'Ghana', 'Qatar', 'Mozambique', 'Lesotho', 'Belgium', 'Bahamas', 'Argentina', 'Sierra Leone', 'France', 'Cameroon', 'Malawi', 'Jersey', 'Panama', 'Hungary', 'Isle of Man', 'Gambia', 'Papua New Guinea', 'Canada', 'Mexico', 'Costa Rica', 'Luxembourg', 'Fiji', 'Botswana', 'Greece', 'Cayman Islands', 'Saudi Arabia', 'South Korea', 'St Helena', 'Cambodia', 'Mali', 'Israel', 'Barbados', 'Slovenia', 'Turkey', 'Iran']
 
# Calculate player win ratios for the specified teams
top_5_win_ratios_df = calculate_player_win_ratios(data_dir, teams_to_include)

# Save the top 5 players per team to a CSV file
top_5_win_ratios_df.to_csv('top_5_player_win_ratios_T20.csv', index=False)