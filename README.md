---
Title: "Load Management in the NBA: Does It Work?"
Authors: "Nathan Catalano and Christian Swoop"
Date: "5/03/2026"
Output: "Python File"
GitHub Link: "https://github.com/5cswoop5/Drake_NBA_Project"
---

## Introduction
This repository contains the code and data necessary to reproduce the results in our white paper titled "Load Management in the NBA: Does It Work?". Specifically, it is used to make the necessary data cleaning, transformations, and regression models we ran. 

## Project Summary
This project is aimed to address a prevelant topic in recent years within the NBA, does load managment actually work? Load managment in the NBA is the strategic manipulation of important players minutes usually during the later part of the season, that helps tanking teams lose more games. This is also done by playoff teams who have clinched playoff seeding to rest players for a playoff run. The purpose of such actions for tanking teams is to gain a higher proability of a lottery pick in the following year's draft and for winning teams lead to deeper playoff runs. Additional research such as limiting injury severity and recovery timelines could be conducted with this data.

In our analysis we created metrics based on NBA data to capture minute / game manipulation by teams in different parts of the season, to ultimately use as independent variables in a regression on our dependent variable draft pick in the tanking teams model and on our depedent variable playoff wins for our winning teams model.


## Data Sources

 ####   Kaggle (Sourced From Basketball Reference)- All Data was from 1947 - 2024
 https://www.kaggle.com/datasets/gonzalogigena/nba-all-time-stats

 1. Schedule Data - This dataset contained results of all games played all time in the NBA. This data included metrics such as scores, win / loss records, playoff / regular season indicators, date the game was played, and what season the game was played in. (2025-2026 data sourced directly from Basketball Reference)

 2. Box Scores - This dataset included quarter, half, and game totals for each player in the team's active roster during that season. This data included overall statistics regarding offensive and defensive performance, along with minutes played.

 3. Total Stats - This data set is an aggregate statistics for each player in a given season. Including games played and started, along with offensive and defensive metrics. (2025-2026 data sourced directly from Basketball Reference)

 ####  Injury Report (2021-2026)
https://official.nba.com/nba-injury-report-2025-26-season/
 

 1. This dataset includes reported injuries by game and player from the 2021 season and forward. Data included team and player names, date of the injury, ID and date of the game.

 ####  Injured List (1990-2021)
 https://www.kaggle.com/datasets/loganlauton/nba-injury-stats-1951-2023

 1. This dataset shows all players listed on injured reserved from 1951 to 2023. Data was used from 1990-2021 to match rest of project. This dataset is listed at the player and season level showing the date the player was initially put on the list , what the desciption of their injury was, and which team they were a part of.

 #### Lottery Data
 https://basketball.realgm.com/nba/draft/lottery_results/2025

 1. This dataset shows the year of the draft, the team who originally was given that pick number, their odds of the #1 overall pick, their pre-draft pick position, the player selected, and which team actually made the pick. 

# Pre-Processing Steps
## Steps for PowerBI Dashboard

1. Injury Report clean up needed due to Python code not perfectly reading PDF.
+ Normalization of team rows was needed, done using Find and Replace in Excel (ex. AtlantaHawks to Atlanta Hawks)
+ Manual adjustments were needed to adjust awkward creation of new rows (approx 100 rows affected). This occurred when the Reason column did not follow the structure of "Injury/Illness-Injury Body Part;Injury Type". This occurred when multiple injuries were reported. (ex. Injury/Illness-Right Knee; Soreness; Injury Management)
+ Binary columns created to count games missed, management days used based on Reason column stating "Management, Maintenance, and Rest", G League column created to filter out those rows in PowerBI
2. GameIDs were created on Injury Report, Schedule, and Box Score tables to join later in PowerBI
3. Function created in excel to calculate team's record, column later unpivoted to separate wins/losses and home/visitor
4. Teams reference table was added in order account for variances in datasets using team abbreviations or full team names
5. Return date calculated on 1990-2021 injuries table (IR). This was calculated by Excel XLOOKUP in BoxScores to find the date the player returned to game action post injury date

## Steps for Python models
1. Appending Box Score Data
+ Exported initial files from Kaggle into one zip file.
+ Loaded in pandas and os packages
+ Unzipped the file and wrote code to read the file path, looking for only the file names that ended in "_Basic". 
+ Extracted the start year of the season the file represented as each file followed the same naming convention (i.e.,NBA_2021-2022_basic). 
+ Filtered only for files that were from 1990 and forward and tagged each row of data with it's respective season in a "2021-2022" format. 
+ Appended all files into one data frame.
+ Saved to CSV as boxscores_1990_fwd_games_only

2. Schedule Initial Data Scrub
+ Exported Data from Kaggle - all seasons were included in one file, so appending needed.
+ Loaded in pandas
+ Loaded into python using read csv command
+ Transformed date of when the game was played to date time format
+ Extracted Wins and losses from Home & Visitor teams' records using string split, converting the string to an integer.
+ Attendance values were stored as strings (i.e., 20,111), so we replaced commas with blanks, filled in blank values, and converted values to integers.
+ Defined Winner column using point total (Home PTS > Visitor Points) then Home team is Winner, and vice versa. If points were even, then we defined it as a tie (There were none)
+ Recreated our own unique game identifier to connect other data sources, did so using a concatenation of date, visiting team, and home team. 
+ Defined NBA Finals indicator using series description provided (If series == 'Finals' then 1 else 0)
+ Reformatted record strings (i.e., 4-2) so that when exported out excel would not read as date
+ Saved to CSV as NBA_Schedule_Scrubbed

3. Schedule Data Unpivot + further transformations
+ Uploaded packages pandas, numpy, seasborn, and matplotlib
+ Uploaded NBA_Schedule_Scrubbed from step 2
+ Created two copies of the dataset, one for home teams, and one for away teams, to make modeling easier by team. Data was originally structured so that teams populate in both the home and visitor team columns. Creating duplicate data sets allowed us to focus on each team in one column.
+ Renamed columns in both data sets to identify which team was the team of focus (i.e, in Home data set: Home Team = Team, in Away dataset Visitor Team = "Team"). Also renamed points and records to match the nomenclature. 
+ Appended the datasets
+ Removed duplicate instances of games, after our transformation each unique game should have two instances, we removed any duplicates with more than two instances. 
+ Filtered for only games from seasons 1990 - 2024.
+ Added Season outlier indicators for NBA seasons which did not have complete 82 game seasons. Defined the seasons in a data frame then merged that back into our dataset to create a binary indicator.
+ Converted Winner binary from true / false to 1 or 0 (integer)
+ Sorted data by Team and Date
+ Used groupby Team & Date to determine how many games were between the last played game and created back-to-back game binary for when the value was equal to one (or 1 day ago was the last time that team played a game)
+ Turned playoff binary from true/false to 1 or 0 (integer) 
+ Created play-in flag to identify games played in-between regular season and playoffs so that they were not accounted for in regular season metrics. Did so by defining a binary variable for when the playoff flag = 0 and the team's record was blank.
+ Defined regular season game order by using a groupby by on our dataset filtered for when playoffs & play in flags both equaled 0 on season, team, and date then ranking the values
+ Added column for total regular season games for each team grouping by team, season, and date the aggregating number of unique instances.
+ Defined late season games as when game order > .65 * Season game count. In laments terms defined the last 35% of games as the late season.

4. Box Score Data Transformations + Schedule data merge
+ Loaded in boxscores_1990_fwd_games_only csv from step 1
+ Changed Starter indicator from True / False to binary (0/1)
+ Created a new minutes played column extracting the first two characters from each string then converted to numeric value.
+ Merged schedule data including all the transformed columns mentioned in section 3, such as playoff flag, finals flag, back-to-back flag, winning team, game order, season outlier, play in flag, etc.
+ Created everyday starter flag by grouping box score data by team, season, and player reference, defined games started and games played. Then added start percentage (games started / games played), then defined everyday starters as players who started at least 70% of the games. Merged this list back into box scores and made it a binary variable.
+ Created star player flag, using same grouping as everyday starters but instead defining points per game, games played, and the number of games for that team in a given season. Added on availability rate (games played / total season games). Then filtered data for only players with availability >= 70% and with 20 or more points per game. Merged back into box scores to create binary flag. Filled any null or NA values with 0.
+ Added star player columns for when star binary indicator = 1, including minutes & points. Did same for everyday starters.
+ Created bench player binary indicator for when starter flag = 0
+ Created bench columns like others including minutes and points
+ Converted original points and all created points columns (Star, everyday starter, and bench) to numeric and coerced values to be in the same format.
+ Defined rest columns for everyday starter, star, and bench players for when minutes were less than 25.
+ Defined championship teams by grouping by team season and winning team for when finals flag = 1. Aggregated wins and then filtered for instances when wins = 4 to define champions. Merged into team season data set (defined in bullets below)
+ Created data set for team-season totals (from box score data), aggregating rest games, minutes, and minutes per game for each subcategory (Star, everyday starter, and bench players) for both the early season (when late season =0) and for the late season to use for comparison. Also aggregated the sum of star player instances (used to define star player binary mentioned below).
+  Aggregated team-season totals (from schedule data) to include games played, early & late season games, wins, early & late season wins, back-to-back games, play-in games, play-in wins, playoff games and playoff wins.
+  Merged the team-season totals from both data sets to get one combined data set showing all results by team & season.
+  Created early & late season columns including early & late season percent of minutes played (for stars, everyday starters, starters, and bench players). Used these columns to calculate difference in ratio for each category to see if the ratio increased or decreased in the late vs. the early season (ex. Star late season % of minutes played - Star early season % of minutes played).
+ Created columns defining the teams early & late season win percentage (i.e., Early season wins / early season games)
+ Created columns for late season rest percentage for each subcategory (stars & everyday starters), (i.e., late season rest games / late season games).
+ Created columns for MPG difference in similar fashion to minutes played. Did so for everyday starters and stars. (i.e., Late Season MPG - Early Season MPG)
+ Added star player binary for when sum of the star player column was greater than 0

5. Added Lottery data to team season data set
+ Loaded in lottery data from CSV file.
+ Lottery odds were stored as string (i.e., 20%) stripped the numeric value from the string, converted to float, and divided by 100 to get decimal value (i.e., .20)
+ Dropped unnecessary columns.
+  Merged lottery results into team season data
+  Exported final file to CSV as nba_team_season_predictors_late_seasonV7
+  Note two versions of this file were used for the regression but the only difference is additional columns, you can use V7 for both regressions. 

6. Regression - Tanking Teams
+ Loaded in nba_team_season_predictors_late_seasonV7 from CSV.
+ Loaded in packages : pandas, NumPy, statsmodels.api, seaborn, matplotlib.pyplot, sklearn.linear_model, sklearn metrics, sklearn processing (Did not use sk packages) 
+ Dropped categorical columns (Team, Season) 
+ Filtered for instances when playoff flag = 0 and dropped the column
+ Ran correlation matrix on all numeric variables using sns heatmap function.
+ Dropped highly correlated variables
+ Ran second correlation matrix to ensure no multicollinearity.
+ Ran 5 different OLS models changing predictors but keeping draft pick number ("Pick") as the dependent variable using the statsmodels.api package.
+ Ran one model with late season win pct as the dependent variable.
+ Finalized model included: Predictors (Late Season Win PCT, Star Player minutes PCT variance, everyday starter minutes PCT variance, everyday starter late season minutes PCT and bench minutes PCT varaiance) Dependent (Draft Pick)
+ Put results from model into data frame using pandas and appended R squared, ADJ R squared, and f statistic. Then exported results to CSV


7. Regression - Winning Teams
+ Loaded in nba_team_season_predictors_late_seasonV7 from CSV
+ Loaded in packages : pandas, NumPy, statsmodels.api, seaborn, matplotlib.pyplot, sklearn.linear_model, sklearn metrics, sklearn processing (Did not use sk packages)
+ Dropped categorical columns (Team, Season)
+ Filtered for instances when playoff games > 0
+ Ran correlation matrix using sns heatmap function.
+ Created interaction variable for Star Late Season Rest Percentage & Late Season Win PCT (Star Late Season Rest Percentage * Late Season Win PCT)
+ Ran two OLS regression models using the statsmodels.api package with Playoff Wins as the dependent variable.
+ Created team clustered standard error for the final model using cov_type = 'cluster; and cov_kwds = ['groups': teams]
+ The model with clustered standard errors was the final model, used pandas to get results into data frame and appended R squared, ADJ R squared, and f statistic. Then exported results to CSV.

# Modeling Decisions
## Data Structure
1. For visualization, active table relationships are as followed:
+ BoxScores_1 [many to 1] Schedule on GameID
+ Injuries Combined [many to 1] Schedule on GameID
+ New Injury Report [many to 1] Schedule on GameID
+ Old Injuries [many to many] Teams on Team Name
+ Old Injuries Updated [many to 1] Schedule on GameID
+ Schedule [many to 1] Date Table on Date
+ Schedule [many to many] Stats on Season

  
2. For Regressions
+ Since load management is typically done by certain teams, we felt aggregating the data at the team and season level would be the best way to use the data for a regression model
+ Using the schedule data, we got team statistics that were not player specific such as total, regular season, playoff, and play in games. To then use these values as denominators in many of our calculations.
+ The box score data was used to get player specific data, define subcategories such as stars, everyday starters, bench, and starters. Using this data, we were able to aggregate statistics by sub-category to then create ratios by combining the overall team data with the player specific data.

## Regression Models
+ For simplicity of interpretation we decided to use an OLS regression model since our dependent variable in both sets of regressions were numeric.
+ Deciding the predictor or independent variables was done by using correlation matrices to avoid multicollinearity but also using anecdotal knowledge of what we thought would be best to predict the variance in our dependent variables.
+ Expanding on the anecdotal knowledge, for the tanking model we needed to define variables which indicated that teams were manipulating rosters in the late part of the season. The best way we thought of doing this was minutes played ratio compared to the overall minutes played, as games played would not show that teams were intentionally playing certain subcategories of players more or less. Furthermore, using a ratio of rest games which we defined earlier was an effective way of seeing how many games were teams minimizing sub-categories of players minutes, rather than just comparing how they played players in the early part of the season compared to later on.
+ For the winning team’s model, the same process ensued but some of variables we used were not relevant to winning playoff games, so certain variables were dropped and others were added. However, the logic remained the same: which metrics would best indicate a team was strategically changing or resting certain sub-categories of players.

# Instructions for a 3rd Party to Replicate This Analysis

## For PowerBI
1. Stats and Teams tables merged via merge queries on Abbreviation, expanded to include full team name. Rows filtered that were blank (ex. TOT for players who played on multiple teams that season. Split stats remained)
2. Player Name column created on Stats table transform original player name to standard characters and remove accents for consistency purposes
3. Season column required adjustment on schedule table for consistency purposes for 2021-2026. Ex("2021-22" to "2021-2022").
4. Season column added to Old Injuries table to prep for merge with New Injury Report
5. Nested left outer join for Schedule and Old Injuries table on Season column to get game by game injury log
6. Injuries combined table created with Old Injuries Updated and New Injury Report tables to get full game by game injury report from 1990-2026.
7. A separate date table created to create a Season Month column to create monthly charts in season order. (October-September)
8. Calculated values for End of Season Record and Playoff Record were created to allow for those records to be reflected based on which season/team were selected on the slicer


## For Regressions in Python
1. Export schedule data and box score zip from kaggle  https://www.kaggle.com/datasets/gonzalogigena/nba-all-time-stats
2. Unzip box score file in your saved folder
3. Run Appending_Boxscores_1990_fwd_games_only Python Source file but change read CSV source to your respective file path where the appended box score file is saved
4. Save appended box score CSV from the above python file output
5. Run NBA_Schedule_scrub, again changing read CSV source to your respective file path where the schedule export is saved
6. Save scrubbed schedule file
7. Run NBA_Data_Merge ensuring the file paths for both the scrubbed schedule and appended box score data are updated to the correct file path
8. Save output from NBA_Data_Merge this is the team season level aggregations used to run regressions
9. Run NBA_Regression_Tanking updating the file path and file name to the export from NBA data merge
10. Save CSV output from this file and this will be the final regression results
11. Run NBA_Regression_Winning, updating the file path and file name to the export from NBA data merge
12. Save CSV output from this file and this will be the final regression results



