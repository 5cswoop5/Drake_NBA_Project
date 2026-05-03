import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# reading file
schedule = pd.read_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_schedule_scrubbed.csv")
print(schedule.head())
print(schedule.columns)


# creating copy of each game for home & away teams, then renaming columns to be consistent for both home and away teams, 
# and adding a column to indicate if the team is playing at home or away
home = schedule.copy()
away = schedule.copy()

home = home.rename(columns=({"Home":"Team","Home PTS":"PTS","Home Record":"Record","Home Wins":"Wins","Home Losses":"Losses",
                             "Visitor":"Opponent","Visitor PTS":"Opponent PTS","Visitor Record":"Opponent Record","Visitor Wins":"Opponent Wins","Visitor Losses":"Opponent Losses"}))


home["is_home"] = 1

away = away.rename(columns=({"Visitor":"Team","Visitor PTS":"PTS","Visitor Record":"Record","Visitor Wins":"Wins","Visitor Losses":"Losses",
                             "Home":"Opponent","Home PTS":"Opponent PTS","Home Record":"Opponent Record","Home Wins":"Opponent Wins","Home Losses":"Opponent Losses"}))

away["is_home"] = 0


#Appending Data sets 
team_game = pd.concat([home, away], ignore_index=True)

# Checking for duplicates
Game_Check = team_game.groupby("GameID").size()

bad_games = Game_Check[Game_Check != 2]
print(bad_games)

duplicated_game = team_game[team_game["GameID"] == "19540308_BLB@MLH"]
print(duplicated_game)

# Removing duplicates
team_game_clean = team_game[team_game["GameID"] != "19540308_BLB@MLH"]

print(team_game_clean[team_game_clean["GameID"] == "19540308_BLB@MLH"])


# Filtering for only season between 1990-2024
team_game_clean = team_game_clean[
    (team_game_clean["Season"] >= "1990-1991") &
    (team_game_clean["Season"] <= "2023-2024")
]

print(team_game_clean.head())

# Checking if filter was successful
team_game_season = team_game_clean.groupby("Season").size()
print(team_game_season)


# Add outlier column for seasons with less than 82 games (Lockouts & COVID))
outlier_seasons = ["1998-1999","2011-2012", "2019-2020","2020-2021"]

team_game_clean["Season_Outlier"] = team_game_clean["Season"].isin(outlier_seasons)

#team_game_stats.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\team_game_statsv2.csv", index=False, encoding="utf-8-sig") 

# Adding Binary column for whether the team won the game or not
team_game_clean["Winning_Team"] = team_game_clean["Team"] == team_game_clean["Winner"]
team_game_clean["Winning_Team"] = team_game_clean["Winning_Team"].astype(int)


print(team_game_clean[["Team", "Winner", "Winning_Team"]].head(50))


print(team_game_clean.dtypes)


# Converting Date column to datetime format
team_game_clean['Date'] = pd.to_datetime(team_game_clean['Date'])


# Sorting Data by Team & Date
team_game_clean = team_game_clean.sort_values(by=['Team', 'Date'])


# Calculating Days Since Last Game for each team
team_game_clean["Days_Since_Last_Game"] = team_game_clean.groupby("Team")["Date"].diff().dt.days

print(team_game_clean[["Team", "Date", "Days_Since_Last_Game"]].head(50))


# Back to Back game flag
team_game_clean["Back_to_Back"] = (team_game_clean["Days_Since_Last_Game"] == 1).astype(int)

print(team_game_clean[["Team", "Date", "Days_Since_Last_Game", "Back_to_Back"]].head(50))


# Changing playoff indicator to binary
team_game_clean["Playoff_Flag"] = team_game_clean["Playoffs"].astype(int)

# Adding play in game indicator
team_game_clean["Play-in_Flag"] = ( team_game_clean["Playoffs"] == 0) & (team_game_clean["Record"].isna()).astype(int)


# Rank regular season games within each season
team_game_clean["Game_Order"] = (
    team_game_clean[(team_game_clean["Playoff_Flag"] == 0)& (team_game_clean["Play-in_Flag"] == 0)].groupby(["Season", "Team"])["Date"].rank(method="dense")
)

# Regular season games per season
team_game_clean["Season_Game_Count"] = (
    team_game_clean[(team_game_clean["Playoff_Flag"] == 0)& (team_game_clean["Play-in_Flag"] == 0)].groupby(["Season", "Team"])["Date"].transform("nunique")
)

# Late season threshold (last 25%)
team_game_clean["Late_Season"] = (
    team_game_clean["Game_Order"] > 0.65 * team_game_clean["Season_Game_Count"]
).astype(int)


# Exclude playoffs
team_game_clean["Late_Season"] = team_game_clean["Late_Season"] * (team_game_clean["Playoff_Flag"] == 0).astype(int)


# Changing Finals indicator to binary
team_game_clean["Finals_Flag"] = team_game_clean["Finals"].astype(int)


print(team_game_clean.head(50))


team_game_clean = team_game_clean.drop(columns=["Playoffs", "Finals", "Start (ET)"])




# Loading in box scores data
box_scores = pd.read_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_combined_boxscores_1990_fwd_games_only.csv")
print(box_scores.head())


# Filtering box scores for same time fram
box_scores = box_scores[(box_scores["season"] >= "1990-1991") & 
                        (box_scores["season"] <= "2023-2024")]


# Checking if filter was successful
box_scores_grouped = box_scores.groupby("season").size()
print(box_scores_grouped)


# Changing Starter indicator to binary
box_scores["Starter_B"] = box_scores["Starter"].astype(int)
print(box_scores[["Starter", "Starter_B"]].head(50))


box_scores["Starter"] = box_scores["Starter"].astype(int)
box_scores = box_scores.drop(columns=["Starter_B"])


print(box_scores.columns)

#Cleaning Minutes played columns
uniq_minutes= box_scores["MP"].unique()
#pd.DataFrame(uniq_minutes, columns=["MP"]).to_csv(
 #   r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_minutes_played_unique_values.csv",
  #  index=False,
   # encoding="utf-8-sig"
#)

# Converting minutes played to numeric values
box_scores["Minutes"] = (
    box_scores["MP"]
    .astype(str)
    .str.extract(r"(\d+):", expand=False)
    .astype(float)
)

print(box_scores[["MP", "Minutes"]].head(50))

print(box_scores.columns)

print(box_scores.head(50))

# Joining  Schedule information to Box scores
team_game_ID = team_game_clean[["Game Reference","Team","GameID","Playoff_Flag","Finals_Flag","Late_Season","Back_to_Back",
                                "Winning_Team","Game_Order","Season_Game_Count","Season_Outlier","Days_Since_Last_Game","Play-in_Flag"
                                ]].drop_duplicates()

box_scores = pd.merge(
   box_scores,
  team_game_ID,
   on=["Game Reference","Team"],
  how="left")    

print(box_scores.head(50))

# Checking for duplicate player names within the same game
game_Player = box_scores.groupby(["Game Reference","Player Name"]).size().reset_index(name="Count")
game_duplicates = game_Player[game_Player["Count"] > 1]
print(game_duplicates)

duplicate_rows = box_scores.merge(
    game_duplicates[["Game Reference","Player Name"]],
    on=["Game Reference","Player Name"],
    how="inner"
)

print(duplicate_rows)

# Creating a everyday starter flag

everyday_starters = ( box_scores[box_scores["Playoff_Flag"] == 0].groupby(["season", "Team","Player Reference"] ).agg(
    Games_Started = ("Starter", "sum"),
    Games_Played = ("Starter", lambda x: x[box_scores.loc[x.index,"Minutes"] > 0].count())
).reset_index())

# Creating Start % based on games startred & games played
everyday_starters["Start_PCT`"] = everyday_starters["Games_Started"] / everyday_starters["Games_Played"]


# Everday starter flag for players who started at least 70% of the games they played in a season for a team
everyday_starters["Everyday_Starter"] = (everyday_starters["Start_PCT`"] >= 0.7).astype(int)


# Merging Everyday Starter indicator back to box scores
box_scores = box_scores.merge(
    everyday_starters[[
        "season", "Team", "Player Reference", "Everyday_Starter"
    ]],
    on=["season", "Team", "Player Reference"],
    how="left"
)


# Add star player indicator column (If player averages 20 or more points per game in the season)

# Grouping Player stats by season and team (accounts for trades within a season)
player_season_stats = ( box_scores[box_scores["Playoff_Flag"] == 0].groupby(["season", "Team","Player Reference"] ).agg(
        PPG=("PTS", "mean"),
        GP =("PTS", "count"),
        Season_Games = ("Season_Game_Count", "max")
    )).reset_index()

# Defijning Availability Rate for each player on each team and season
player_season_stats["Availability Rate"]= (player_season_stats["GP"] / player_season_stats["Season_Games"])


# Defining star player as someone who has played 70% of the team's games and scored 20ppg while on that team in that season
player_season_stats["Star_Player"] = (player_season_stats["Availability Rate"] >= 0.7) & (player_season_stats["PPG"] >= 20).astype(int)

#player_season_stats.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_player_season_stats.csv", index=False, encoding="utf-8-sig")


# Merging Star Player indicator back to box scores
box_scores = box_scores.merge(
    player_season_stats[[
        "season", "Team", "Player Reference", "Star_Player"
    ]],
    on=["season", "Team", "Player Reference"],
    how="left"
)

print(box_scores[box_scores["Star_Player"] == 1][["Player Name", "season", "Team", "PTS", "Star_Player"]].tail(50))

# Filling NA values in Star Player column with 0 (indicating not a star player) and converting to integer
box_scores["Star_Player"] = box_scores["Star_Player"].fillna(0)
box_scores["Star_Player"] = box_scores["Star_Player"].astype(int)


print(box_scores.columns)


#Adding Star Player Minutes 
box_scores["Star_Minutes"] = box_scores["Minutes"] * box_scores["Star_Player"]

# Adding Star Player Points
box_scores["Star_PTS"] = box_scores["PTS"] * box_scores["Star_Player"]



#Adding Starter Minutes column
box_scores["Starter_Minutes"] = box_scores["Minutes"] * box_scores["Starter"]
print(box_scores[["Minutes", "Starter", "Starter_Minutes"]].head(50))


# Add Bench Player Indicator column
box_scores["Bench_Player"] = (box_scores["Starter"] == 0).astype(int)
print(box_scores[["Starter", "Bench_Player"]].head(50))


# Adding Bench Minutes column
box_scores["Bench_Minutes"] = box_scores["Minutes"] * box_scores["Bench_Player"]
print(box_scores[["Minutes", "Starter", "Starter_Minutes", "Bench_Player", "Bench_Minutes"]].head(50))


# Adding Starter/ Bench Points Columns
box_scores["Starter_PTS"] = box_scores["PTS"] * box_scores["Starter"]
box_scores["Bench_PTS"] = box_scores["PTS"] * box_scores["Bench_Player"]
print (box_scores[["PTS", "Starter", "Starter_PTS", "Bench_Player", "Bench_PTS"]].head(50))




# Converting Points to numeric
box_scores["PTS"] = pd.to_numeric(box_scores["PTS"], errors="coerce")
box_scores["Starter_PTS"] = pd.to_numeric(box_scores["Starter_PTS"], errors ="coerce")  
box_scores["Bench_PTS"] = pd.to_numeric(box_scores["Bench_PTS"], errors="coerce")   


print(box_scores.columns)

print(box_scores[["Player Name","Starter","Star_Player","Bench_Player","PTS","Starter_Minutes","Bench_Minutes","Star_Minutes","Starter_PTS","Bench_PTS","Star_PTS"]].tail(50))


# Everyday Starter Rest Indicator (If everyday starter played less than 25 minutes in a game)
box_scores["Everyday_Starter_Rest"] = ((box_scores["Everyday_Starter"] == 1) & (box_scores["Minutes"] < 25)).astype(int)

# Starter Rest Indicator (If starter played less than 25 minutes in a game)
box_scores["Starter_Rest"] = ((box_scores["Starter"] == 1) & (box_scores["Minutes"] < 25)).astype(int)

# Star Rest Indicator (If star player played less than 25 minutes in a game)
box_scores["Star_Rest"] = ((box_scores["Star_Player"] == 1) & (box_scores["Minutes"] < 25)).astype(int)


print(box_scores["Winning_Team"].head(50))

# Indentifying the teams which won the finals in their season

team_game_finals = team_game_clean[team_game_clean["Finals_Flag"] == 1][["Season", "Team", "Winning_Team"]]

team_game_finals =team_game_finals.groupby(["Season", "Team"])["Winning_Team"].sum().reset_index(name="Wins")

champions = team_game_finals[team_game_finals["Wins"] == 4]

print(champions)

#Team_season_totals = box_scores.groupby(["season", "Team"]).agg(

#box_scores.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_box_scores_enhanced.csv", index=False, encoding="utf-8-sig")


# Aggregating box score data to team-season level, separating early and late season stats, and calculating rest games for star players and starters in early and late season
team_season_totals = box_scores.groupby(["season", "Team"]).agg(
    Star_Players = ("Star_Player", "sum"),
    Star_Early_Rest_Games = ("Star_Rest", lambda x: x[box_scores.loc[x.index,"Late_Season"] == 0].sum()),
    Everyday_Starter_Early_Rest_Games = ("Everyday_Starter_Rest", lambda x: x[box_scores.loc[x.index,"Late_Season"] == 0].sum()),
    Starter_Early_Rest_Games = ("Starter_Rest", lambda x: x[box_scores.loc[x.index,"Late_Season"] == 0].sum()),


    Early_Season_Minutes = ("Minutes", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 0].sum()),
    Star_Early_Season_Minutes = ("Star_Minutes", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 0].sum()),
    Everyday_Starter_Early_Season_Minutes = ("Minutes", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 0) & (box_scores.loc[x.index,"Everyday_Starter"]==1)].sum()),
    Starter_Early_Season_Minutes = ("Starter_Minutes", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 0].sum()),
    Bench_Early_Season_Minutes = ("Bench_Minutes", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 0].sum()),

    Star_Early_Season_MPG = ("Star_Minutes", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 0) & (box_scores.loc[x.index,"Star_Player"]==1)].mean()),
    Everyday_Starter_Early_Season_MPG = ("Minutes", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 0) & (box_scores.loc[x.index,"Everyday_Starter"]==1)].mean()),
    Starter_Early_Season_MPG = ("Starter_Minutes", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 0) & (box_scores.loc[x.index,"Starter"]==1)].mean()),
    Bench_Early_Season_MPG = ("Bench_Minutes", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 0)&(box_scores.loc[x.index,"Bench_Player"]==1)].mean()),

    #Star_Early_Season_PPG = ("Star_PTS", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 0) & (box_scores.loc[x.index,"Star_Player"]==1)].mean()),
    #Starter_Early_Season_PPG = ("Starter_PTS", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 0) & (box_scores.loc[x.index,"Starter"]==1)].mean()),
    #Bench_Early_Season_PPG = ("Bench_PTS", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 0)&(box_scores.loc[x.index,"Bench_Player"]==1)].mean()),

    Star_Late_Games = ("Star_Player", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 1].sum()),
    Star_Late_Rest_Games = ("Star_Rest", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 1].sum()),
    Starter_Late_Rest_Games = ("Starter_Rest", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 1].sum()),
    Everyday_Starter_Late_Games = ("Everyday_Starter", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 1].sum()),
    Everyday_Starter_Late_Rest_Games = ("Everyday_Starter_Rest", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 1].sum()),

    Late_Season_Minutes = ("Minutes", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 1].sum()),
    Star_Late_Season_Minutes =("Star_Minutes", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 1].sum()),
    Starter_Late_Season_Minutes = ("Starter_Minutes", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 1].sum()),
    Bench_Late_Season_Minutes = ("Bench_Minutes", lambda x: x[box_scores.loc[x.index, "Late_Season"] == 1].sum()),
    Everyday_Starter_Late_Season_Minutes = ("Minutes", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 1) & (box_scores.loc[x.index,"Everyday_Starter"]==1)].sum()),

    Star_Late_Season_MPG = ("Star_Minutes", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 1) & (box_scores.loc[x.index,"Star_Player"]==1)].mean()),
    Starter_Late_Season_MPG = ("Starter_Minutes", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 1) & (box_scores.loc[x.index,"Starter"]==1)].mean()),
    Bench_Late_Season_MPG = ("Bench_Minutes", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 1)&(box_scores.loc[x.index,"Bench_Player"]==1)].mean()),
    Everyday_Starter_Late_Season_MPG = ("Minutes", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 1) & (box_scores.loc[x.index,"Everyday_Starter"]==1)].mean()),

    #Star_Late_Season_PPG = ("Star_PTS", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 1) & (box_scores.loc[x.index,"Star_Player"]==1)].mean()),
    #Starter_Late_Season_PPG = ("Starter_PTS", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 1) & (box_scores.loc[x.index,"Starter"]==1)].mean()),
    #Bench_Late_Season_PPG = ("Bench_PTS", lambda x: x[(box_scores.loc[x.index, "Late_Season"] == 1)&(box_scores.loc[x.index,"Bench_Player"]==1)].mean()),

).reset_index()

print(team_season_totals.tail(50))


#Renaming season column to match team_game_clean for merging later
team_season_totals = team_season_totals.rename(columns={"season": "Season"})


# Aggregating team game data to team-season level to get total wins, losses, games played, back to back games, playoff games, play in games, and late season games, and then merging with champions data to identify which teams won the championship in each season
team_game_totals = team_game_clean.groupby(["Season", "Team",]).agg(
  Games = ("Winning_Team", "count"),
  Early_Season_Games = ("Winning_Team", lambda x: x[(team_game_clean.loc[x.index,"Late_Season"]==0) & (team_game_clean.loc[x.index,"Playoff_Flag"]==0) & (team_game_clean.loc[x.index,"Play-in_Flag"]==0)].count()),
  Late_Season_Games = ("Late_Season","sum"),
  Wins = ("Winning_Team", "sum"),
  Early_Season_Wins = ("Winning_Team", lambda x: x[(team_game_clean.loc[x.index,"Late_Season"]==0) & (team_game_clean.loc[x.index,"Playoff_Flag"]==0) & (team_game_clean.loc[x.index,"Play-in_Flag"]==0)].sum()),
  Late_Season_Wins = ("Winning_Team", lambda x: x[team_game_clean.loc[x.index,"Late_Season"]==1].sum()),
  Back_to_Back_Games = ("Back_to_Back", "sum"),
  Play_in_Games = ("Play-in_Flag", "sum"),
  Play_in_Wins = ("Winning_Team", lambda x: x[team_game_clean.loc[x.index, "Play-in_Flag"] == 1].sum()),
  Playoff_Games = ("Playoff_Flag", "sum"),
  Playoff_Wins = ("Winning_Team", lambda x: x[team_game_clean.loc[x.index, "Playoff_Flag"] == 1].sum())).reset_index()

team_game_totals["Regular_Season_Games"] = team_game_totals["Games"] - team_game_totals["Play_in_Games"] - team_game_totals["Playoff_Games"]
team_game_totals["Regular_Season_Wins"] = team_game_totals["Wins"] - team_game_totals["Play_in_Wins"] - team_game_totals["Playoff_Wins"]
team_game_totals["Regular_Season_Losses"] = team_game_totals["Regular_Season_Games"] - team_game_totals["Regular_Season_Wins"]



# Merging champions data to team game totals to identify which teams won the championship in each season
team_game_totals = team_game_totals.merge(
    champions[["Season", "Team"]].assign(Champions=1),
    on=["Season", "Team"],
    how="left",
).fillna({"Champions": 0})


# Converting Champions column to integer type
team_game_totals["Champions"] = team_game_totals["Champions"].astype(int)

print(team_game_totals.tail(50))


# Condensing team game totals to only the columns needed for merging with team season totals and creating predictors for modeling
team_game_total_condensed = team_game_totals[["Season", "Team","Early_Season_Games","Late_Season_Games", "Back_to_Back_Games",
                                              "Regular_Season_Wins", "Regular_Season_Losses","Playoff_Games","Playoff_Wins",
                                                "Champions", "Early_Season_Wins", "Late_Season_Wins"]]

print(team_game_total_condensed.tail(50))

# Merging team game totals with team season totals to have all the necessary information in one dataset for modeling
team_season_totals = team_season_totals.merge(
    team_game_total_condensed,
    on=["Season", "Team"],
    how="left"
)

print(team_season_totals.tail(50))


# Rounding minutes columns to 1 decimal place for easier interpretation and analysis
team_season_totals = team_season_totals.round(1)


# Creating new columns for star player minutes as a percentage of total minutes in early and late season, the variance between the two
team_season_totals["Star_Early_Season_Minutes_PCT"] = team_season_totals["Star_Early_Season_Minutes"] / team_season_totals["Early_Season_Minutes"]

team_season_totals["Star_Late_Season_Minutes_PCT"] = team_season_totals["Star_Late_Season_Minutes"] / team_season_totals["Late_Season_Minutes"]

team_season_totals["Star_Minutes_PCT_Variance"] = team_season_totals["Star_Late_Season_Minutes_PCT"] - team_season_totals["Star_Early_Season_Minutes_PCT"]

team_season_totals["Star_MPG_Variance"] = team_season_totals["Star_Late_Season_MPG"] - team_season_totals["Star_Early_Season_MPG"]


# Creating new column for star player rest games as a percentage of total late season games to capture the impact of star player rest on late season performance
team_season_totals["Star_Late_Season_Rest_PCT"] = team_season_totals["Star_Late_Rest_Games"] / team_season_totals["Star_Late_Games"]


# Creating column for team early win PCT and late win PCT to capture the impact of team performance in early vs late season
team_season_totals["Early_Season_Win_PCT"] = team_season_totals["Early_Season_Wins"] / team_season_totals["Early_Season_Games"]

team_season_totals["Late_Season_Win_PCT"] = team_season_totals["Late_Season_Wins"] / team_season_totals["Late_Season_Games"]


# Choosing selected predictor columns for modeling and analysis
team_season_predictors_stars = team_season_totals[["Season", "Team","Early_Season_Win_PCT", "Late_Season_Win_PCT", "Star_Early_Season_Minutes_PCT", 
        "Star_Late_Season_Minutes_PCT", "Star_Minutes_PCT_Variance", "Star_Late_Season_Rest_PCT", "Star_Late_Season_MPG","Star_Late_Rest_Games"]]

#team_season_predictors.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_team_season_predictorsV1.csv", index=False, encoding="utf-8-sig")


# Creating new columns for starter player minutes as a percentage of total minutes in early and late season, the variance between the two
team_season_totals["Starter_Early_Season_Minutes_PCT"] = team_season_totals["Starter_Early_Season_Minutes"] / team_season_totals["Early_Season_Minutes"]

team_season_totals["Starter_Late_Season_Minutes_PCT"] = team_season_totals["Starter_Late_Season_Minutes"] / team_season_totals["Late_Season_Minutes"]

team_season_totals["Starter_Minutes_PCT_Variance"] = team_season_totals["Starter_Late_Season_Minutes_PCT"] - team_season_totals["Starter_Early_Season_Minutes_PCT"]




# Creating new columns for bench player minutes as a percentage of total minutes in early and late season, the variance between the two
team_season_totals["Bench_Early_Season_Minutes_PCT"] = team_season_totals["Bench_Early_Season_Minutes"] / team_season_totals["Early_Season_Minutes"]

team_season_totals["Bench_Late_Season_Minutes_PCT"] = team_season_totals["Bench_Late_Season_Minutes"] / team_season_totals["Late_Season_Minutes"]

team_season_totals["Bench_Minutes_PCT_Variance"] = team_season_totals["Bench_Late_Season_Minutes_PCT"] - team_season_totals["Bench_Early_Season_Minutes_PCT"]



# Choosing selected predictor columns for modeling and analysis
team_season_predictors_starters = team_season_totals[["Season", "Team","Early_Season_Win_PCT", "Late_Season_Win_PCT","Playoff_Games",
      "Star_Late_Season_Minutes_PCT", "Star_Minutes_PCT_Variance", "Star_Late_Season_Rest_PCT","Star_Late_Rest_Games",
        "Starter_Late_Season_Minutes_PCT", "Starter_Minutes_PCT_Variance","Starter_Late_Rest_Games", "Starter_Late_Season_MPG"]]

#team_season_predictors_starters.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_team_season_predictors_startersV3.csv", index=False, encoding="utf-8-sig")

# Creating Everday Starter predictors for modeling and analysis
team_season_totals["Everyday_Starter_Early_Season_Minutes_PCT"] = team_season_totals["Everyday_Starter_Early_Season_Minutes"] / team_season_totals["Early_Season_Minutes"]

team_season_totals["Everyday_Starter_Late_Season_Minutes_PCT"] = team_season_totals["Everyday_Starter_Late_Season_Minutes"] / team_season_totals["Late_Season_Minutes"]

team_season_totals["Everyday_Starter_Minutes_PCT_Variance"] = team_season_totals["Everyday_Starter_Late_Season_Minutes_PCT"] - team_season_totals["Everyday_Starter_Early_Season_Minutes_PCT"]

team_season_totals["Everyday_Starter_Late_Season_Rest_PCT"] = team_season_totals["Everyday_Starter_Late_Rest_Games"] / team_season_totals["Everyday_Starter_Late_Games"]

team_season_totals["Everyday_Starter_MPG_Variance"] = team_season_totals["Everyday_Starter_Late_Season_MPG"] - team_season_totals["Everyday_Starter_Early_Season_MPG"]


#eam_season_totals.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_team_season_totals.csv", index=False, encoding="utf-8-sig")


# Star Player Binary Indicator (if team has at least 1 star player in the season)
team_season_totals["Star_Player_Binary"] = (team_season_totals["Star_Players"] > 0).astype(int)


team_late_season_predictors = team_season_totals[["Season", "Team","Regular_Season_Wins","Late_Season_Wins",
                                                  "Early_Season_Win_PCT", "Late_Season_Win_PCT","Playoff_Games","Playoff_Wins",
      "Star_Late_Season_Minutes_PCT", "Star_Minutes_PCT_Variance", "Star_Late_Season_Rest_PCT","Star_Late_Rest_Games","Star_MPG_Variance",
      "Everyday_Starter_Late_Season_Minutes_PCT", "Everyday_Starter_Minutes_PCT_Variance","Everyday_Starter_MPG_Variance",
        "Everyday_Starter_Late_Season_Rest_PCT","Everyday_Starter_Late_Rest_Games",
      "Bench_Late_Season_Minutes_PCT", "Bench_Minutes_PCT_Variance","Star_Player_Binary"
      ]]

#team_late_season_predictors.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_team_season_predictors_late_seasonV1.csv", index=False, encoding="utf-8-sig")


# Load in Lottery data
lottery = pd.read_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\Lottery_Data.csv")

# Changing drafrt year to indicate the season prior that led to the draft (e.g. 1990 draft would be 1989 season)
lottery["Season"] = (
    (lottery["Year"] - 1).astype(str) + "-" +
    lottery["Year"].astype(str)
)

print(lottery.head())

print(lottery.dtypes)

# Stripping % sign from odds column and converting to numeric values
lottery["Revised Odds"] = lottery["Odds"].str.rstrip("%").astype(float) / 100

print(lottery[["Odds", "Revised Odds"]].head(50))

# Dropping unecessary columns
lottery = lottery.drop(columns=["Year", "Odds","Player Taken", "Draft Team","Record"])


# Renaming columns
lottery = lottery.rename(columns={"Revised Odds": "Lottery_Odds"})

print(lottery.head())

# Merging lottery data to team late season predictors
team_late_season_predictors = team_late_season_predictors.merge(
    lottery[["Season", "Team", "Lottery_Odds","Pick"]],
    on=["Season", "Team"],
    how="left"
)

print(team_late_season_predictors.head(50))

team_late_season_predictors.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_team_season_predictors_late_seasonV7.csv", index=False, encoding="utf-8-sig")


# Checking data types
print(team_late_season_predictors.dtypes)

#print(box_scores.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_box_scores_enhancedV2.csv", index=False, encoding="utf-8-sig"))
