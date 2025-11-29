import pandas as pd

def split_valid_invalid(df):
    copiedDF = df.copy()
    copiedDF['home_team_ranking'].fillna(-1, inplace=True)
    copiedDF['away_team_ranking'].fillna(-1, inplace=True)

    null_row_mask = copiedDF.isna().any(axis=1)
    invalid_df = copiedDF[null_row_mask].copy()
    valid_df = copiedDF[~null_row_mask].copy()

    return [valid_df, invalid_df]

def clean_valid_df(df):
    cleaned_df = df.dropna().drop_duplicates().copy()
    cleaned_df['home_team_mascot'].fillna('N/A', inplace=True)
    cleaned_df['away_team_mascot'].fillna('N/A', inplace=True)

    return cleaned_df