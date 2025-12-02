import pandas as pd

def split_valid_invalid(df):
    copiedDF = df.copy()
    copiedDF['home_team_ranking'] = copiedDF['home_team_ranking'].fillna(-1)
    copiedDF['away_team_ranking'] = copiedDF['away_team_ranking'].fillna(-1)
    copiedDF['home_team_mascot'] = copiedDF['home_team_mascot'].fillna('N/A')
    copiedDF['away_team_mascot'] = copiedDF['away_team_mascot'].fillna('N/A')


    null_row_mask = copiedDF.isna().any(axis=1)
    invalid_df = copiedDF[null_row_mask].copy()
    valid_df = copiedDF[~null_row_mask].copy()

    return [valid_df, invalid_df]

def clean_valid_df(df):
    cleaned_df = df.drop_duplicates().copy()
    return cleaned_df