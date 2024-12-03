import pandas as pd

# Load the CSV file
df = pd.read_csv('/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/T20/Data_Preprocessing_and_Collection/T20_international_data.csv')

# Filter rows where 'bat_first' is 1 (first innings)
df_first_innings = df[df['bat_first'] == 1]

# Select the required columns
reduced_df = df_first_innings[['match_id', 'batting_team', 'bowling_team', 'city', 'final_score', 'outcome', 'bat_first']]

# Drop duplicates to ensure one row per match_id
reduced_df = reduced_df.drop_duplicates(subset=['match_id'])

# Save the reduced DataFrame to a new CSV file
reduced_df.to_csv('model_2_t20_data.csv', index=False)

# Display the first few rows of the resulting DataFrame
print(reduced_df.head(50))