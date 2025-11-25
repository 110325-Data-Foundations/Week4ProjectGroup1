import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv('DATABASE_URL')

engine = create_engine(database_url)

cfbdf = pd.read_sql_query('SELECT g.*,ht.id as home_team_id,ht.name_full as home_team_full_name,ht.name_school as home_team_school_name, ht.mascot as home_team_mascot, at.id as away_team_id, at.name_full as away_team_full_name, at.name_school as away_team_school_name, at.mascot as away_team_mascot FROM games g JOIN teams ht ON ht.id = g.id_home_team JOIN teams at ON at.id = g.id_away_team;', engine)
#cfbdf.to_csv("./data/cfb_data.csv", index=False)
#cfbdf.to_json("./data/cfb_data.json")