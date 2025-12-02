import pandas as pd
import os 
from dotenv import load_dotenv
from . import validation as vd
from . import process_sources as process
from . import writing_to_db as wr

def main():
    raw_sources = process.load_source()[0]
    raw_f = process.read_source(raw_sources['CSV'])
    valid_d, invalid_d = vd.split_valid_invalid(raw_f)
    cleaned_d = vd.clean_valid_df(valid_d)

    cleaned_d.to_csv('./data/CLEANED.CSV', index=False)
    cleaned_d.to_json('./data/CLEANED.JSON', index=False)
    invalid_d.to_csv('./data/INVALID.CSV', index=False)
    
    teams_df = wr.build_teams_df(cleaned_d)
    games_df = wr.build_games_df(cleaned_d)

    with process.get_engine() as engine:
        wr.build_tables(teams_df,games_df,invalid_d, engine)
        
if __name__ == "__main__":
    main()