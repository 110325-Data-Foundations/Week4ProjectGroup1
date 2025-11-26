import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv('DATABASE_URL')

engine = create_engine(database_url)
query = """
SELECT 
    g.*,
    ht.id as home_team_id,
    ht.name_full as home_team_full_name,
    ht.name_school as home_team_school_name, 
    ht.mascot as home_team_mascot, 
    at.id as away_team_id, 
    at.name_full as away_team_full_name, 
    at.name_school as away_team_school_name, 
    at.mascot as away_team_mascot, 
    hr.ranking as home_team_ranking, 
    ar.ranking as away_team_ranking 
    FROM games g 
    JOIN teams ht ON ht.id = g.id_home_team 
    JOIN teams at ON at.id = g.id_away_team 
    LEFT JOIN 
        (SELECT hr.team_id, hr.year, hr.week, hr.postseason, hr.ranking FROM rankings hr WHERE poll = 'AP Top 25') hr
        ON hr.team_id = ht.id AND hr.year = g.year AND hr.week = g.week AND hr.postseason = g.postseason 
    LEFT JOIN 
        (SELECT ar.team_id, ar.year, ar.week, ar.postseason, ar.ranking FROM rankings ar WHERE poll = 'AP Top 25') ar 
        ON ar.team_id = at.id AND ar.year = g.year AND ar.week = g.week AND ar.postseason = g.postseason;
"""

cfbdf = pd.read_sql_query(query, engine)
cfbdf.to_csv("./data/cfb_data.csv", index=False)
cfbdf.to_json("./data/cfb_data.json", orient='records')