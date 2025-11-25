import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv('DATABASE_URL')

engine = create_engine(database_url)

games_df = pd.read_sql_table('games', engine)
games_df.to_csv("games.csv", index=False)
