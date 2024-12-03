from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
import pandas as pd

# my own file path below
df = pd.read_csv('/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/ODI/Data_Preprocessing_and_Collection/all_odi_data.csv')

#relative file path
#df = pd.read_csv('../Data_Preprocessing_and_Collection/all_odi_data.csvv')

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
pipe_chasing_outcome = Pipeline(steps=[
    ('preprocessor', transformer),  # Preprocess the features
    ('classifier', XGBClassifier(n_estimators=500, learning_rate=0.1, max_depth=8, random_state=1))  # Classifier
])

# Train the model
pipe_chasing_outcome.fit(X_train, y_train)

# Predict outcomes
y_pred = pipe_chasing_outcome.predict(X_test)

# Predict probabilities of winning
y_pred_proba = pipe_chasing_outcome.predict_proba(X_test)[:, 1]  # Probability of winning (positive class)

# Evaluate the model
print("Outcome Prediction Accuracy:", accuracy_score(y_test, y_pred))
#print("Outcome Prediction ROC AUC:", roc_auc_score(y_test, y_pred_proba))
print("Outcome Prediction Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

import pickle
pickle.dump(pipe_chasing_outcome,open('MODEL_3_ODI.pkl','wb'))

