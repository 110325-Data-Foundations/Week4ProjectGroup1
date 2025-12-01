import pandas as pd
import os 
from dotenv import load_dotenv
import validation as vd
import process_sources as process

def main():
    raw_sources = process.load_source()[0]
    raw_f = process.read_source(raw_sources['CSV'])
    valid_d, invalid_d = vd.split_valid_invalid(raw_f)
    cleaned_d = vd.clean_valid_df(valid_d)

    cleaned_d.to_csv('./data/cleaned_cfb_data.csv', index=False)
    cleaned_d.to_json('./data/cleaned_cfb_data.json', index=False)
    invalid_d.to_csv('./data/invalid_data.csv', index=False)

if __name__ == "__main__":
    main()
