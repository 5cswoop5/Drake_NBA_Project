# Importing packages
from xml.parsers.expat import model

import pandas as pd
import numpy as np
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# Loading data
nba_predictors = pd.read_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_team_season_predictors_late_seasonV6.csv")

# Displaying top rows
print(nba_predictors.head())

# Check data types
print(nba_predictors.dtypes)

# Dropping categorical variables for regression analysis
nba_predictors_numeric =nba_predictors.drop(columns=['Team', 'Season'])

#Only look at teams who did not make the playoffs
nba_predictors_numeric = nba_predictors_numeric[nba_predictors_numeric['Playoff_Games'] == 0]

nba_predictors_numeric = nba_predictors_numeric.drop(columns=['Playoff_Games'])

# Run correlation matrix
correlation_matrix = nba_predictors_numeric.corr()
print(correlation_matrix)

# First Correlation Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    center=0,
    linewidths=0.5,
    annot_kws={"size": 8}
)
plt.title('Predictor correlation matrix')
plt.tight_layout()
plt.show()


# Dropping highly correlated predictors
nba_predictors_numeric = nba_predictors_numeric.drop(columns=['Early_Season_Win_PCT', 'Star_Late_Rest_Games',"Everyday_Starter_Late_Rest_Games",
                                                              "Lottery_Odds","Star_Player_Binary"])

# Correlation matrix #2
correlation_matrix = nba_predictors_numeric.corr()
print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    center=0,
    linewidths=0.5,
    annot_kws={"size": 8}
)
plt.title('Predictor correlation matrix')
plt.tight_layout()
plt.show()


# Look at remaining predictors
print(nba_predictors_numeric.columns)


# Setting predictors and target variable
predictors = ['Late_Season_Win_PCT',
       'Star_Minutes_PCT_Variance', "Everyday_Starter_Minutes_PCT_Variance",
       "Everyday_Starter_Late_Season_Minutes_PCT",
       "Bench_Minutes_PCT_Variance", ]

X = nba_predictors_numeric[predictors]
y = nba_predictors_numeric['Pick']

# Drop NaNs from both X and y at the same time
mask = X.notna().all(axis=1) & y.notna()
X = X[mask]
y = y[mask]

# Model 1 - OLS regression
X_const = sm.add_constant(X)
modelf= sm.OLS(y, X_const).fit()
print(modelf.summary())

# Setting predictors and target variable
predictors_v2 = [
       'Star_Minutes_PCT_Variance', 'Star_Late_Season_Rest_PCT',
       'Everyday_Starter_Minutes_PCT_Variance',
       'Everyday_Starter_Late_Season_Rest_PCT',
       "Everyday_Starter_Late_Season_Minutes_PCT",
       'Bench_Late_Season_Minutes_PCT', 'Bench_Minutes_PCT_Variance']

X = nba_predictors_numeric[predictors_v2]
y = nba_predictors_numeric['Pick']

# Drop NaNs from both X and y at the same time
mask = X.notna().all(axis=1) & y.notna()
X = X[mask]
y = y[mask]

# Model 2 - OLS regression removing Late Season win PCT to see if roster managment variables are significant without controlling for team performance
X_const = sm.add_constant(X)
model_v2 = sm.OLS(y, X_const).fit()
print(model_v2.summary())


# Creating interaction term between Late Season Win PCT and Everday Starter Late Season Rest PCT
nba_predictors_numeric['Win_PCT_x_Everyday_Starter_Rest'] = nba_predictors_numeric['Late_Season_Win_PCT'] * nba_predictors_numeric['Everyday_Starter_Late_Season_Rest_PCT']


# Setting predictors and target variable
predictors_v3 = ['Win_PCT_x_Everyday_Starter_Rest', 
                 'Late_Season_Win_PCT',
                 'Everyday_Starter_Late_Season_Rest_PCT',
                 "Everyday_Starter_MPG_Variance",
       'Star_Minutes_PCT_Variance', 'Star_Late_Season_Rest_PCT',
       'Everyday_Starter_Minutes_PCT_Variance',
       "Everyday_Starter_Late_Season_Minutes_PCT",
       'Bench_Late_Season_Minutes_PCT', 'Bench_Minutes_PCT_Variance']

X = nba_predictors_numeric[predictors_v3]
y = nba_predictors_numeric['Pick']

# Drop NaNs from both X and y at the same time
mask = X.notna().all(axis=1) & y.notna()
X = X[mask]
y = y[mask]

# Model 3 - OLS regression with interaction term
X_const = sm.add_constant(X)
model_v3 = sm.OLS(y, X_const).fit()
print(model_v3.summary())


# Reduce dataset to only teams with top 6 picks to see if predictors are significant within this group
nba_predictors_top6 = nba_predictors_numeric[nba_predictors_numeric['Pick'] <= 6]

# Setting predictors and target variable
predictors_v4 = ["Everyday_Starter_MPG_Variance",
       'Star_Minutes_PCT_Variance', 'Star_Late_Season_Rest_PCT',
       'Everyday_Starter_Minutes_PCT_Variance',
       'Everyday_Starter_Late_Season_Rest_PCT',
       "Everyday_Starter_Late_Season_Minutes_PCT",
       'Bench_Late_Season_Minutes_PCT', 'Bench_Minutes_PCT_Variance']

X = nba_predictors_top6[predictors_v4]
y = nba_predictors_top6['Pick']

# Drop NaNs from both X and y at the same time
mask = X.notna().all(axis=1) & y.notna()
X = X[mask]
y = y[mask]

# Model 4 - OLS regression for top 6 picks
X_const = sm.add_constant(X)
model_v4 = sm.OLS(y, X_const).fit()
print(model_v4.summary())


#Limiting the data set to more modern year
nba_predictors_modern = nba_predictors[nba_predictors['Season'] >= '2015-2016']

nba_predictors_modern_numeric = nba_predictors_modern.drop(columns=['Team', 'Season', 'Playoff_Games'])



# Setting predictors and target variable
predictors_v5 = ["Late_Season_Win_PCT","Everyday_Starter_MPG_Variance",
       'Star_Minutes_PCT_Variance', 'Star_Late_Season_Rest_PCT',
       'Everyday_Starter_Minutes_PCT_Variance',
       'Everyday_Starter_Late_Season_Rest_PCT',
       "Everyday_Starter_Late_Season_Minutes_PCT",
       'Bench_Late_Season_Minutes_PCT', 'Bench_Minutes_PCT_Variance']

X = nba_predictors_modern_numeric[predictors_v5]
y = nba_predictors_modern_numeric['Pick']

# Drop NaNs from both X and y at the same time
mask = X.notna().all(axis=1) & y.notna()
X = X[mask]
y = y[mask]

# Model 5 - OLS regression for modern era
X_const = sm.add_constant(X)
model_v5 = sm.OLS(y, X_const).fit()
print(model_v5.summary())



# Switcing Dependent Variable to Late Season Win PCT to see if roster management variables are significant predictors of team performance

# Setting predictors and target variable
predictors_v6 = [
       'Star_Minutes_PCT_Variance', 'Star_Late_Season_Rest_PCT',
       'Everyday_Starter_Minutes_PCT_Variance',
       'Everyday_Starter_Late_Season_Rest_PCT',
       "Everyday_Starter_Late_Season_Minutes_PCT",
       "Everyday_Starter_MPG_Variance",
       'Bench_Late_Season_Minutes_PCT', 'Bench_Minutes_PCT_Variance']

X = nba_predictors_modern_numeric[predictors_v6]
y = nba_predictors_modern_numeric['Late_Season_Win_PCT']

# Drop NaNs from both X and y at the same time
mask = X.notna().all(axis=1) & y.notna()
X = X[mask]
y = y[mask]

# Model 6 - OLS regression for modern era
X_const = sm.add_constant(X)
model_v6 = sm.OLS(y, X_const).fit()
print(model_v6.summary())


results_df = pd.DataFrame({
    'Variable': modelf .params.index,
    'Coefficient': modelf. params.values.round(4),
    'Std Error': modelf.bse.values.round(4),
    'z-stat': modelf.tvalues.values.round(4),
    'P-value': modelf.pvalues.values.round(4),
    'CI Lower': modelf.conf_int()[0].values.round(4),
    'CI Upper': modelf.conf_int()[1].values.round(4)
})

# Append model fit stats as rows
fit_stats = pd.DataFrame({
    'Variable': ['R-squared', 'Adj. R-squared', ' Prob (F-statistic)'],
    'Coefficient': [round(modelf.rsquared, 4), round(modelf.rsquared_adj, 4), modelf.f_pvalue ],
    'Std Error': ['', '', ''],
    'z-stat': ['', '', ''],
    'P-value': ['', '', ''],
    'CI Lower': ['', '', ''],
    'CI Upper': ['', '', '']
})

results_df = pd.concat([results_df, fit_stats], ignore_index=True)


#results_df.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_losers_regression_results.csv", index=False)



