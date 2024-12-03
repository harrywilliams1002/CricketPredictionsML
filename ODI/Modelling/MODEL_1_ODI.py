#This model predicts the final score of the first innings for a mens ODI match

from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error

#my own file path below
df = pd.read_csv('/Users/Harry/Documents/Harry_Hawkeye/New_double_innings_approach/ODI/Data_Preprocessing_and_Collection/all_odi_data.csv')

#relative file path
#df = pd.read_csv('../Data_Preprocessing_and_Collection/all_odi_data.csv')

df_odi_batfirst = df[df['bat_first'] == 1]

X_odi = df_odi_batfirst[['balls_left', 'wickets_left', 'run_rate', 'runs', 'batting_team', 'bowling_team', 'city']]
y_odi = df_odi_batfirst['final_score']

X_train, X_test, y_train, y_test = train_test_split(X_odi, y_odi, test_size=0.2, random_state=42)

# Train XGBoost model
transformer = ColumnTransformer([
    ('transformer', OneHotEncoder(sparse_output=False, drop='first'), ['batting_team', 'bowling_team', 'city'])
], remainder='passthrough')
pipe_batfirst_odi_score=Pipeline(steps=[
    ('step1',transformer),
    ('step2',StandardScaler()),
    ('step3', XGBRegressor(n_estimators=1000, learning_rate=0.2,max_depth=12,random_state=1))
])
pipe_batfirst_odi_score.fit(X_train,y_train)
y_pred=pipe_batfirst_odi_score.predict(X_test)

print(r2_score(y_test, y_pred))
print(mean_absolute_error(y_test, y_pred))

import pickle
#pickle.dump(pipe_batfirst_odi_score,open('MODEL_1_ODI.pkl','wb'))