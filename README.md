---
Title: "NBA Load Managment : Does Tanking Lead to a Higher Draft Pick?"
Authors: "Nathan Catalano and Christian Swoop"
Date: "5/03/2026"
Output: "Python File"
---

## Introduction
This repository contains the code and data necessary to reproduce the results in our white paper titled "NBA Load Managment : Does Tanking Lead to a Higher Draft Pick?". Specifically, it is used to make the necessary data cleaning, transformations, and regression models we ran. 

## Project Summary
This project is aimed to address a prevelant topic in recent years within the NBA, does load managment actually work. Load managment in the NBA is the intentional manipulation of important players minutes usually during the later part of the season, that helps teams lose more games. The purpose of such actions is to gain a higher proability of a lottery pick in the following year's draft.

In our analysis we created metrics based on NBA data to capture minute / game manipulation by teams in different parts of the season, to ultimately use as independent variables in a regression on our dependent variable draft pick.


## Data Sources

 ####   Kaggle (Sourced From Basketball Reference)- All Data was from 1947 - 2024

 1. Schedule Data - This dataset contained results of all games played all time in the NBA. This data included metrics such as scores, win / loss records, playoff / regular season indicators, date the game was played, and what season the game was played in.

 2. Box Scores - This dataset included quarter,half, and game totals for each player in the team's active roster during that season. This data included overall statistics regarding offensive and defensive performance, along with minutes played.

 3. Total Stats - This data set is an aggregate statistics for each player in a given season. Including games played and started, along with offensive and defensive metrics.

 ####  Injury Report (Sourced Directly From the NBA)

 1. This dataset includes reported injuries by game and player from the 2021 season and forward. Data included team and player names, date of the injury, ID and date of the game.

 ####  Injured List (Need Source from Nathan)

 1. This dataset shows all players listed on injured reserved from 1990 to 2021. This dataset is listed at the player and season level showing the date the player was initially put on the list , what the desciption of their injury was, and which team they were a part of.

 #### Lottery Data

 1. This dataset shows the year of the draft, the team who originally was given that pick number, their odds of the #1 overall pick, their pre-draft pick position, the player selected, and which team actually made the pick. 

## Pre-Processing Steps

1. Nathan talk about injury data transformations, game ID creation, connecting tables, etc.

2. Appending Box Score Data
+ Exported initial files from Kaggle into one zip file.
+ Unzipped the file and wrote code to read the file path, looking for only the file names that ended in "_Basic". 
+ Extracted the start year of the season the file represented as each file followed the same naming convention (i.e.,NBA_2021-2022_basic). 
+ Filtered only for files that were from 1990 and forward and tagged each row of data with it's respect seaon in a "2021-2022" format. 
+ Appeneded all files into one data frame.

3. Schedule Initital Data Scrub
+ Transformed date of when the game was played to date time format
+ Extracted Wins and losses from Home & Visitor teams' records using string split, converting the string to an integer
+ Attendance values were stored as strings (i.e., 20,111), so we replaced commas with blanks, filled in blank values, and converted values to integers
+ Defined Winner column using point total (Home PTS > Visitor Points) then Home team is Winner,and vice versa. If points were even then we defined it a tie (There were none)
+ Recreated our own unique game identifer to connect other data sources, did so using a concatenation of date, visiting team, and home team. 
+ Defined NBA Finals indicator using series description provided (If series == 'Finals' then 1 else 0)
+ Reformatted string records (i.e., 4-2) so that when exported out excel would not read as date

4. Schedule Data Unpivot + further transformations
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

