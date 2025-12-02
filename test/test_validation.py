import pandas as pd 
from ..processing import validation as vd

def test_split_valid_invalid_correctly():
    df = pd.DataFrame({
        'id': [10,20,30],
        'home_team_ranking': [1, None, 5],
        'away_team_ranking': [3, 2, None],
        'home_team_full_name': ['Tiger', 'Bear', None]
    })

    valid, invalid = vd.split_valid_invalid(df)

    assert len(valid) == 2
    assert not valid['home_team_ranking'].isna().any()
    assert not valid['away_team_ranking'].isna().any()
    assert not valid['home_team_full_name'].isna().any()

    assert len(invalid) == 1
    assert not invalid['home_team_ranking'].isna().any()
    assert not invalid['away_team_ranking'].isna().any()
    assert invalid['home_team_full_name'].isna().any()

def test_clean_valid_df_correctly():
    df = pd.DataFrame({
        'id': [10,10,30],
        'home_team_mascot': ['Tiger', 'Tiger', 5],
        'away_team_mascot': [2, 2, None],
    })
    cleaned_df = vd.clean_valid_df(df)

    #Need to double check with team
