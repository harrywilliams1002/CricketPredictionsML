from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd

# my own file path below
df = pd.read_csv('/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/ODI/Data_Preprocessing_and_Collection/model_2_ODI_data.csv')

#relative file path
#df = pd.read_csv('../Data_Preprocessing_and_Collection/model_2_ODI_data.csv')

# Features and target
X = df[['final_score', 'batting_team', 'bowling_team', 'city']]
y = df['outcome']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline for categorical encoding and classification
transformer = ColumnTransformer([
    ('encode', OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore'), ['batting_team', 'bowling_team', 'city'])
], remainder='passthrough')

pipe_batfirst_outcome_and_probability = Pipeline(steps=[
    ('transform', transformer),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train the model
pipe_batfirst_outcome_and_probability.fit(X_train, y_train)

# Predict both outcomes and probabilities
y_pred = pipe_batfirst_outcome_and_probability.predict(X_test)
y_pred_proba = pipe_batfirst_outcome_and_probability.predict_proba(X_test)[:, 1]  # Probabilities for batting team win (class=1)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Accuracy:", accuracy)
print("Confusion Matrix:\n", conf_matrix)

import pickle
#pickle.dump(pipe_batfirst_outcome_and_probability,open('MODEL_2_ODI.pkl','wb'))
