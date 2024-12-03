 I have created an application for predicting the scoring and outcomes of cricket matches, given certain scenarios.

 The project structure is as follows:

├── /CricketScorePredictor
│   ├── /Flask_App
│   │    ├──models -> Contains my exported models
│   │    ├──static -> Contains styling
│   │    ├──templates -> Contains HTML file for app frontend
│   │    ├──app.py -> Application backend
│   │
│   ├── /ODI
│   │     ├──Data_Preprocessing_and_Collection -> All data methods and files for ODI stored here
│   │     ├──Modelling -> All modelling processes for ODI are stored here
│   │     ├──Models -> Exported ODI models stored here
│   │
│   ├── /T20
│   │     ├──Data_Preprocessing_and_Collection -> All data methods and files for T20 stored here
│   │     ├──Modelling -> All modelling processes for T20 are stored here
│   │     ├──Models -> Exported T20 models stored here
│   │
│   ├── /PlayerRatios -> CSVs containing data used for tables in application regarding win ratios
│   ├── /Scorers -> CSVs containing data used for tables in application regarding top total runs scorers
│   ├── /Batting_First_ODI_example -> A video example of the application being used for an ODI match, batting first
│   ├── /Chasing_T20_example -> A video example of the application being used for a T20 match, second innings


Modelling:
- I chose to focus on two forms of international cricket, T20 and ODIs.
- I felt that as strategy and play style can vary wildly in these two different formats it was wise to model them seperately.
- I collected data from the jsons folders using the files created in my Data_Preprocessing_and_Collection (I have not included the T20_jsons and odi_jsons folders here as they are extremely large).
- I decided to create three seperate models for each for each format for three seperate things:

Model 1: Predict the final score of an innings if you are batting first.
(Trained on balls left, wickets left, run rate, runs, batting team, bowling team and city to predict the final score)

Model 2: Predict the outcome of the match, and the probability of that outcome, given the current score in the first innings.
(This model takes the prediction from model 1 as an input and therefore is trained on final score, batting team, bowling team and city to predict the outcome)

Model 3: Predict the outcome of a match, and the probability of that outcome, given the current score in the second innings, and the target score.
(Trained on target score, balls left, wickets left, run rate, runs, batting team, bowling team and city to predict the final score)

- For all of these models categorical features were selected and encoded; batting team, bowling team and city.
- XGBoost was utilised to train these models due to its combination of speed, flexibility, ability to handle diverse datasets and predictive accuracy. Model 1 utilised XGBRegressor whilst Models 2 and 3 utilised XGBClassifier.

Model Evaluation Results:

Model 1 ODI: 
R^2 score - 0.9731059670448303 : Explains approximately 97.31% of the variance in ODI cricket scores, indicating a highly accurate fit to the data.
Mean absolute error - 4.272005665280657 : On average, the model's predictions deviate from the actual scores by around 4.27 runs

Model 2 ODI:
Accuracy score: 0.7328605200945626 : Correctly predicts the outcome of ODI matches 73.29% of the time, indicating a good but not perfect classification performance
Confusion Matrix:   [[171  57] 
			        [56  139]]

Model 3 ODI:
Accuracy score: 0.9402369617937893 : Correctly predicts the outcome of ODI matches 94.02% of the time, indicating a very good classification performance
Confusion Matrix: [[58896  3910]
			       [3409 56252]]

Model 1 T20:
R^2 score - 0.9697539210319519 : Explains approximately 96.98% of the variance in T20 cricket scores, indicating a highly accurate fit to the data.
Mean absolute error - 3.348307866861699 : On average, the model's predictions deviate from the actual scores by around 4.27 runs.

Model 2 T20:
Accuracy score: 0.6906906906906907 : Correctly predicts the outcome of ODI matches 73.29% of the time, indicating a good classification performance. This could be improved, but shows the unpredictable nature of this format.
Confusion Matrix:   [[119  45]
			        [58  111]]

Model 3 T20:
Outcome Prediction Accuracy: 0.9284785952999841 : Correctly predicts the outcome of ODI matches 92.84% of the time, indicating a very good classification performance
Outcome Prediction Confusion Matrix:
 [[38579  2683]
 [ 2710 31432]]
 			

Improvements:
- I attempted to hyperparamter tune these models, specifically using GridSearchCV to locate the optimal model paramters, but did not have the computer power or time for this method to be completed.
- To improve I would train on additional features such as players. I would include input fetures such as the bowler, with models trained on their historic performance.