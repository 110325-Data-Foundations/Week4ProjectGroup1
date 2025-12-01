import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
import processing.process_sources as process


load_dotenv()
database_url = os.getenv('DATABASE_URL')

engine = create_engine(database_url)

def del_columns(df):
    del df['game_id']
    del df['week']
    del df['points_away']
    del df['points_home']
    del df['id_away_team']
    del df['completed']
    del df['home_team_ranking']
    del df['away_team_ranking']
    del df['postseason']
    del df['conference_game']

games_df = pd.read_sql_table('games', engine)
target_df = games_df.copy(deep=True)
del_columns(target_df)
target_df.rename(columns={'id_home_team': 'team_id'}, inplace=True)
target_df.insert(2,'wins',0)
target_df.insert(3,'ties',0)
target_df.insert(4,'loses',0)
target_df.insert(5,'win_percentage',0)
target_df.insert(6,'point_differential',0)

print(target_df.head())
print(games_df.head())

target_df.drop_duplicates(inplace=True)

for index, row in games_df.iterrows():
    if row['points_home'] == row['points_away']:
        target_df.loc[(target_df['team_id']==row['id_home_team']) & (target_df['year']==row['year']), 'ties'] += 1 
        target_df.loc[(target_df['team_id']==row['id_away_team']) & (target_df['year']==row['year']), 'ties'] += 1
    elif row['points_home'] > row['points_away']:
        target_df.loc[(target_df['team_id']==row['id_home_team']) & (target_df['year']==row['year']), 'wins'] += 1
        target_df.loc[(target_df['team_id']==row['id_home_team']) & (target_df['year']==row['year']), 'point_differential'] += row['points_home']
        target_df.loc[(target_df['team_id']==row['id_home_team']) & (target_df['year']==row['year']), 'point_differential'] -= row['points_away']
        target_df.loc[(target_df['team_id']==row['id_away_team']) & (target_df['year']==row['year']), 'loses'] += 1
        target_df.loc[(target_df['team_id']==row['id_away_team']) & (target_df['year']==row['year']), 'point_differential'] += row['points_away']
        target_df.loc[(target_df['team_id']==row['id_away_team']) & (target_df['year']==row['year']), 'point_differential'] -= row['points_home']
    elif row['points_home'] < row['points_away']:
        target_df.loc[(target_df['team_id']==row['id_home_team']) & (target_df['year']==row['year']), 'loses'] += 1
        target_df.loc[(target_df['team_id']==row['id_home_team']) & (target_df['year']==row['year']), 'point_differential'] += row['points_home']
        target_df.loc[(target_df['team_id']==row['id_home_team']) & (target_df['year']==row['year']), 'point_differential'] -= row['points_away']
        target_df.loc[(target_df['team_id']==row['id_away_team']) & (target_df['year']==row['year']), 'wins'] += 1
        target_df.loc[(target_df['team_id']==row['id_away_team']) & (target_df['year']==row['year']), 'point_differential'] += row['points_away']
        target_df.loc[(target_df['team_id']==row['id_away_team']) & (target_df['year']==row['year']), 'point_differential'] -= row['points_home']


target_df['win_percentage'] = (target_df['wins'] / (target_df['wins'] + target_df['loses'] + target_df['ties']) * 100).round(2)

print(target_df.head())

with process.get_engine() as engine:
        target_df.to_sql(
            "yearly_team",
            con=engine,
            if_exists="append",
            index=False,
        )