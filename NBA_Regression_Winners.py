# Importing packages
import pandas as pd
import numpy as np
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# Loading data
nba_predictors = pd.read_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_team_season_predictors_late_seasonV7.csv")

# Displaying top rows
print(nba_predictors.head())

# Filtering to only include teams that made the playoffs (i.e., Playoff_Games > 0) for the winners regression model
nba_predictors = nba_predictors[nba_predictors["Playoff_Games"] > 0]

# Dropping  variables for regression analysis
nba_predictors_winnersc= nba_predictors.drop(columns=["Team", "Season","Pick","Lottery_Odds","Star_Player_Binary","Everyday_Starter_MPG_Variance","Regular_Season_Wins","Late_Season_Wins","Playoff_Games",
                                                      "Star_Late_Rest_Games","Everyday_Starter_Late_Rest_Games","Bench_Late_Season_Minutes_PCT",'Star_MPG_Variance'])

nba_predictors_winners = nba_predictors.drop(columns=[ "Season","Pick","Lottery_Odds","Star_Player_Binary","Everyday_Starter_MPG_Variance","Regular_Season_Wins","Late_Season_Wins","Playoff_Games",
                                                      "Star_Late_Rest_Games","Everyday_Starter_Late_Rest_Games","Bench_Late_Season_Minutes_PCT",'Star_MPG_Variance'])

nba_predictors_winners["Star_Rest_Late_Win_Interaction"] = nba_predictors_winners["Star_Late_Season_Rest_PCT"] * nba_predictors_winners["Late_Season_Win_PCT"]

# Run correlation matrix
correlation_matrix = nba_predictors_winnersc.corr()
print(correlation_matrix)

# First Correlation Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt='.2f',
    cmap='PuOr',
    center=0,
    linewidths=0.5,
    annot_kws={"size": 8}
)
plt.title('Predictor correlation matrix')
plt.tight_layout()
plt.show()



# Winners Regression Model 1 - OLS regression

predictors_winners= ['Late_Season_Win_PCT', 'Early_Season_Win_PCT',"Star_Rest_Late_Win_Interaction",
                     'Star_Minutes_PCT_Variance', 'Star_Late_Season_Rest_PCT',
                     'Everyday_Starter_Late_Season_Rest_PCT',
                      'Bench_Minutes_PCT_Variance']

X = nba_predictors_winners[predictors_winners]
y = nba_predictors_winners['Playoff_Wins']

# Drop NaNs from both X and y at the same time
mask = X.notna().all(axis=1) & y.notna()
X = X[mask]
y = y[mask]

# Model 1 - OLS regression
X_const = sm.add_constant(X)
model = sm.OLS(y, X_const).fit()
print(model.summary())


# Winners Regression Model 2 - OLS regression (Team Clustered Errors)

predictors_winners= ['Late_Season_Win_PCT', 'Early_Season_Win_PCT',"Star_Rest_Late_Win_Interaction",
                     'Star_Minutes_PCT_Variance', 'Star_Late_Season_Rest_PCT',
                     'Everyday_Starter_Late_Season_Rest_PCT',
                      'Bench_Minutes_PCT_Variance']

X = nba_predictors_winners[predictors_winners]
y = nba_predictors_winners['Playoff_Wins']
teams = nba_predictors_winners['Team']  # pull team column for clustering


# Drop NaNs from both X and y at the same time
mask = X.notna().all(axis=1) & y.notna() & teams.notna()  # also ensure teams column has no NaNs
X = X[mask]
y = y[mask]
teams = teams[mask]  # filter team to match

# Model 2 - OLS regression (Team Clustered Errors)
X_const = sm.add_constant(X)
model = sm.OLS(y, X_const).fit(
    cov_type='cluster',
    cov_kwds={'groups': teams}
)
print(model.summary())


results_df = pd.DataFrame({
    'Variable': model.params.index,
    'Coefficient': model.params.values.round(4),
    'Std Error': model.bse.values.round(4),
    'z-stat': model.tvalues.values.round(4),
    'P-value': model.pvalues.values.round(4),
    'CI Lower': model.conf_int()[0].values.round(4),
    'CI Upper': model.conf_int()[1].values.round(4)
})

# Append model fit stats as rows
fit_stats = pd.DataFrame({
    'Variable': ['R-squared', 'Adj. R-squared', ' Prob (F-statistic)'],
    'Coefficient': [round(model.rsquared, 4), round(model.rsquared_adj, 4), model.f_pvalue ],
    'Std Error': ['', '', ''],
    'z-stat': ['', '', ''],
    'P-value': ['', '', ''],
    'CI Lower': ['', '', ''],
    'CI Upper': ['', '', '']
})

results_df = pd.concat([results_df, fit_stats], ignore_index=True)

results_df.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_winners_regression_results.csv", index=False)