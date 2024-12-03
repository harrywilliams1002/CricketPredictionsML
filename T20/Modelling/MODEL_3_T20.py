from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
import pandas as pd

#my own file path
df = pd.read_csv('/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/T20/Data_Preprocessing_and_Collection/T20_international_data.csv')

#relative file path
#df = pd.read_csv('../Data_Preprocessing_and_Collection/T20_international_data.csv')

# Filter for matches where teams are chasing (second innings)
df_odi_chasing = df[df['bat_first'] == 0]  # Chasing teams

# Features and target for outcome prediction
X_outcome = df_odi_chasing[['runs', 'wickets_left', 'balls_left', 'run_rate', 'batting_team', 'bowling_team', 'city', 'target_score']]
y_outcome = df_odi_chasing['outcome']  # 1 if chasing team wins, 0 otherwise

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_outcome, y_outcome, test_size=0.2, random_state=42)

# Define the transformer for categorical and numerical features
transformer = ColumnTransformer([
    ('categorical', OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore'), 
     ['batting_team', 'bowling_team', 'city']),
    ('numerical', StandardScaler(), ['runs', 'wickets_left', 'balls_left', 'run_rate'])
])

# Define the pipeline
pipe_outcome = Pipeline(steps=[
    ('preprocessor', transformer),  # Preprocess the features
    ('classifier', XGBClassifier(n_estimators=500, learning_rate=0.1, max_depth=8, random_state=1))  # Classifier
])

# Train the model
pipe_outcome.fit(X_train, y_train)

# Predict outcomes
y_pred = pipe_outcome.predict(X_test)

# Predict probabilities of winning
y_pred_proba = pipe_outcome.predict_proba(X_test)[:, 1]  # Probability of winning (positive class)

# Evaluate the model
print("Outcome Prediction Accuracy:", accuracy_score(y_test, y_pred))
print("Outcome Prediction Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# import pickle
# pickle.dump(pipe_outcome,open('MODEL_3_T20.pkl','wb'))

# # Combine results into a DataFrame for analysis
# results = pd.DataFrame({
#     'runs': X_test['runs'].values,
#     'wickets_left': X_test['wickets_left'].values,
#     'balls_left': X_test['balls_left'].values,
#     'run_rate': X_test['run_rate'].values,
#     'target_score': X_test['target_score'].values,
#     'batting_team': X_test['batting_team'].values,
#     'bowling_team': X_test['bowling_team'].values,
#     'city': X_test['city'].values,
#     'actual_outcome': y_test.values,
#     'predicted_outcome': y_pred,
#     'winning_probability': y_pred_proba
# })

# # Display the first few rows of the results
# print(results.head())

# # Example input for a specific game situation
# game_situation = {
#     'runs': [150],  # Current runs scored
#     'wickets_left': [5],  # Wickets left
#     'balls_left': [120],  # Balls remaining
#     'run_rate': [7.5],  # Current run rate
#     'target_score': [385],
#     'batting_team': ['India'],  # Batting team
#     'bowling_team': ['Australia'],  # Bowling team
#     'city': ['Mumbai']  # Match venue
# }

# # Convert the dictionary to a DataFrame
# input_data = pd.DataFrame(game_situation)

# # Predict the likelihood of winning using the trained pipeline
# predicted_proba = pipe_outcome.predict_proba(input_data)[:, 1]  # Probability of winning

# # Output the result
# print(f"Likelihood of winning: {predicted_proba[0] * 100:.2f}%")