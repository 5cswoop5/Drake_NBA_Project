import pandas as pd
import os

folder_path = r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\boxscores_by_year"

files = [
    os.path.join(folder_path, f)
    for f in os.listdir(folder_path)
    if "_basic" in f and f.endswith(".csv")
]

dfs = []

for f in files:
    file_name = os.path.basename(f)

    # Extract season (e.g. 1986-1987 → 1986)
    start_year = int(file_name.split("_")[1].split("-")[0])

    # KEEP ONLY 1980+ seasons
    if start_year < 1990:
        continue

    temp = pd.read_csv(f)

    temp["season"] = file_name.split("_")[1]
    temp["source_file"] = file_name

    dfs.append(temp)

df = pd.concat(dfs, ignore_index=True)

print(df.shape)

print(df.head())

#df.to_csv("nba_combined_boxscores_2020_fwd.csv", index=False)

print(df.dtypes)

nba_games_only = df[df["Period"] == "game"]
#print(nba_games_only.head(50))


#player_unique = nba_games_only["Player Name"].drop_duplicates()
#print(sorted(player_unique))

nba_games_only.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_combined_boxscores_1990_fwd_games_only.csv", index=False,encoding="utf-8-sig")

#player_unique.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_player_names_1990_fwd.csv", index=False,encoding="utf-8-sig")