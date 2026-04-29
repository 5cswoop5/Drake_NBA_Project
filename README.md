---
Title: "Load Management in the NBA: Does It Work?"
Authors: "Nathan Catalano and Christian Swoop"
Date: "5/03/2026"
Output: "Python File"
---

## Introduction
This repository contains the code and data necessary to reproduce the results in our white paper titled "Load Management in the NBA: Does It Work?". Specifically, it is used to make the necessary data cleaning, transformations, and regression models we ran. 

## Project Summary
This project is aimed to address a prevelant topic in recent years within the NBA, does load managment actually work? Load managment in the NBA is the intentional manipulation of important players minutes usually during the later part of the season, that helps teams lose more games. This is also done by playoff teams who have clinched seeding. The purpose of such actions is to gain a higher proability of a lottery pick in the following year's draft or lead to deeper playoff runs? Additional research such as limiting injury severity and recovery timelines could be conducted with this data.

In our analysis we created metrics based on NBA data to capture minute / game manipulation by teams in different parts of the season, to ultimately use as independent variables in a regression on our dependent variable draft pick.


## Data Sources

 ####   Kaggle (Sourced From Basketball Reference)- All Data was from 1947 - 2024
 https://www.kaggle.com/datasets/gonzalogigena/nba-all-time-stats

 1. Schedule Data - This dataset contained results of all games played all time in the NBA. This data included metrics such as scores, win / loss records, playoff / regular season indicators, date the game was played, and what season the game was played in. (2025-2026 data sourced directly from Basketball Reference)

 2. Box Scores - This dataset included quarter,half, and game totals for each player in the team's active roster during that season. This data included overall statistics regarding offensive and defensive performance, along with minutes played.

 3. Total Stats - This data set is an aggregate statistics for each player in a given season. Including games played and started, along with offensive and defensive metrics. (2025-2026 data sourced directly from Basketball Reference)

 ####  Injury Report (2021-2026)
https://official.nba.com/nba-injury-report-2025-26-season/
 

 1. This dataset includes reported injuries by game and player from the 2021 season and forward. Data included team and player names, date of the injury, ID and date of the game.

 ####  Injured List (1990-2021)
 https://www.kaggle.com/datasets/loganlauton/nba-injury-stats-1951-2023

 1. This dataset shows all players listed on injured reserved from 1951 to 2023. Data was used from 1990-2021 to match rest of project. This dataset is listed at the player and season level showing the date the player was initially put on the list , what the desciption of their injury was, and which team they were a part of.

 #### Lottery Data

 1. This dataset shows the year of the draft, the team who originally was given that pick number, their odds of the #1 overall pick, their pre-draft pick position, the player selected, and which team actually made the pick. 

## Pre-Processing Steps
# Steps for PowerBI Dashboard

1. Injury Report clean up needed due to Python code not perfectly reading PDF.
+ Normalization of team rows was needed, done using Find and Replace in Excel (ex. AtlantaHawks to Atlanta Hawks)
+ Manual adjustments were needed to adjust awkward creation of new rows (approx 100 rows affected). This occurred when the Reason column did not follow the structure of "Injury/Illness-Injury Body Part;Injury Type". This occurred when multiple injuries were reported. (ex. Injury/Illness-Right Knee; Soreness; Injury Management)
+ Binary columns created to count games missed, management days used based on Reason column stating "Management, Maintenance, and Rest", G League column created to filter out those rows in PowerBI
2. GameIDs were created on Injury Report, Schedule, and Box Score tables to join later in PowerBI
3. Function created in excel to calculate team's record, column later unpivoted to separate wins/losses and home/visitor
4. Teams reference table was added in order account for variances in datasets using team abbreviations or full team names

# Steps for Python models
1. Appending Box Score Data
+ Exported initial files from Kaggle into one zip file.
+ Unzipped the file and wrote code to read the file path, looking for only the file names that ended in "_Basic". 
+ Extracted the start year of the season the file represented as each file followed the same naming convention (i.e.,NBA_2021-2022_basic). 
+ Filtered only for files that were from 1990 and forward and tagged each row of data with it's respect seaon in a "2021-2022" format. 
+ Appeneded all files into one data frame.

2. Schedule Initital Data Scrub
+ Transformed date of when the game was played to date time format
+ Extracted Wins and losses from Home & Visitor teams' records using string split, converting the string to an integer
+ Attendance values were stored as strings (i.e., 20,111), so we replaced commas with blanks, filled in blank values, and converted values to integers
+ Defined Winner column using point total (Home PTS > Visitor Points) then Home team is Winner,and vice versa. If points were even then we defined it a tie (There were none)
+ Recreated our own unique game identifer to connect other data sources, did so using a concatenation of date, visiting team, and home team. 
+ Defined NBA Finals indicator using series description provided (If series == 'Finals' then 1 else 0)
+ Reformatted string records (i.e., 4-2) so that when exported out excel would not read as date

3. Schedule Data Unpivot + further transformations
+ Created two copies of the dataset, one for home teams, and one for away teams, to make modeling easier by team. Data was originally structued so that teams populate in both the home and visitor team columns. Creating duplicate data sets allowed us to focus on each team in one column. 
+ Renamed columns in both data sets to identify which team was the team of focus (i.e, in Home data set: Home Team = Team, in Away dataset Vistitor Teamm = "Team"). Also renamed points and records to match the nomenclature. 
+ Appended the datasets
+ Removed duplicate instances of games, after our transformation each unique game should have two instances, we removed any duplicates with more than two instances. 
+ Filtered for only games from seasons 1990 - 2024
+ Added Season outlier indicators for NBA seasons which did not have complete 82 game seasons. Defined the seasons in a data frame then merged that back into our dataset to create a binary indicator.
+ Converted Winner binary from true / false to 1 or 0 (integer)
+ Sorted data by Team and Date
+ Used groupby Team & Date to determine how many games were between the last played game and created back to back game binary for when the value was equal to one (or 1 day ago was the last time that team played a game)
+ Turned playoff binary from true/false to 1 or 0 (integer) 
+ Created play-in flag to identify games played inbetween regular season and playoffs so that they were not accounted for in regular season metrics. Did so by defining a binary variable for when the playoff flag = 0 and the team's record was blank.
+ Defined regular season game order by using a groupby by on our dataset filtered for when playoffs & play in flags both equaled 0 on season, team, and date then ranking the values

