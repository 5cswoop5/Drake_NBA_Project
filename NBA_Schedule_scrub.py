## loads the pandas library
import pandas as pd

## loads the titanic dataset 
schedule = pd.read_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\schedule (1).csv")

#Top Rows
print(schedule.head())

# Data Types
print(schedule.dtypes)

# Transforming the Date column to datetime format
schedule['Date'] = pd.to_datetime(schedule['Date'])
print(schedule['Date'])
print(schedule.dtypes)


## Extracting Wins and Losses from Record Columns
schedule ['Home Wins'] = schedule['Home Record'].str.split('-').str[0].astype("Int64")
schedule ['Home Losses'] = schedule['Home Record'].str.split('-').str[1].astype("Int64")

schedule ['Visitor Wins'] = schedule['Visitor Record'].str.split('-').str[0].astype("Int64")
schedule ['Visitor Losses'] = schedule['Visitor Record'].str.split('-').str[1].astype("Int64")


print(schedule.dtypes)

print(schedule['Attendance'].head(20))

# Removing commas from attendance
schedule['Attendance'] = schedule['Attendance'].replace(',', '', regex=True)

# Filling missing values with 0s
schedule['Attendance'] = schedule['Attendance'].fillna(0)

# Converting Attendance to integer
schedule['Attendance'] = pd.to_numeric(schedule['Attendance'], errors='coerce').fillna(0).astype(int)


print(schedule['Attendance'])

print(schedule.dtypes)

# Creating a Winning Team Column based on scores
def winner(row):
    if row['Home PTS'] > row['Visitor PTS']:
        return row['Home']
    elif row['Home PTS'] < row['Visitor PTS']:
        return row['Visitor']
    else:
        return 'Tie'
    
schedule['Winner'] = schedule.apply(winner, axis=1)
print(schedule[['Home', 'Home PTS', 'Visitor', 'Visitor PTS', 'Winner']].head(20))
print(schedule['Winner'].value_counts())

# Checking for ties
schedule_ties = schedule[schedule['Winner'] == 'Tie']
print(schedule_ties.value_counts())
schedule_ties.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_schedule_ties.csv", index=False)


## Creating unique game identifier
schedule['GameID'] = schedule['Date'].dt.strftime('%Y%m%d') + '_' + schedule['Visitor'] + '@' + schedule['Home']
print(schedule['GameID'].head(20))

print(schedule.head(20))

# Defining Championship series games
def finals(row):
    if row['Series'] == 'Finals':
        return True
    elif row['Series'] != 'Finals':
        return False
schedule['Finals'] = schedule.apply(finals, axis=1)
print(schedule[['Series', 'Finals']].head(20))


# Force Formatting Record
schedule['Home Record'] = ' ' + schedule['Home Wins'].astype(str) + '-' + schedule['Home Losses'].astype(str) + ' '
schedule['Visitor Record'] = ' ' + schedule['Visitor Wins'].astype(str) + '-' + schedule['Visitor Losses'].astype(str) + ' '

print(schedule[['Home Record', 'Visitor Record']].head(20))





#Print CSV
schedule.to_csv(r"C:\Users\cswoo_0a3ouyw\OneDrive\Documents\Data\nba_schedule_scrubbed.csv", index=False)