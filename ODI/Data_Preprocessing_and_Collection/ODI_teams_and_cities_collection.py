import pandas as pd

# Load the CSV file
df = pd.read_csv('/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/ODI/Data_Preprocessing_and_Collection/all_odi_data.csv')

# Combine the 'batting_team' and 'bowling_team' columns into one Series and drop duplicates
teams = pd.concat([df['batting_team'], df['bowling_team']]).drop_duplicates()

# Extract unique cities from the 'city' column
cities = df['city'].drop_duplicates()

# Combine teams and cities into a DataFrame
unique_teams_and_cities = pd.DataFrame({
    'Team': teams.reset_index(drop=True),
    'City': cities.reset_index(drop=True)  # Aligns cities and teams side by side
})

# Save the list of unique teams and cities to a new CSV file
unique_teams_and_cities.to_csv('unique_teams_and_cities_ODI.csv', index=False)

# Display the unique teams and cities
#print(unique_teams_and_cities)
