import pandas as pd
from ..processing import writing_to_db as wr
from unittest.mock import MagicMock

def test_build_team_df():
    df = pd.DataFrame({
        "id_home_team": [1, 2],
        "home_team_full_name": ["Team A", "Team B"],
        "home_team_school_name": ["School A", "School B"],
        "home_team_mascot": ["Mascot A", "Mascot B"],
        "id_away_team": [3, 1],
        "away_team_full_name": ["Team C", "Team A"],
        "away_team_school_name": ["School C", "School A"],
        "away_team_mascot": ["Mascot C", "Mascot A"],
    })
    teams_df = wr.build_teams_df(df)

    expected_df = pd.DataFrame({
        'team_id': [1,2,3],
        'full_name': ['Team A', 'Team B', 'Team C'],
        'school_name': ['School A', 'School B', 'School C'],
        'mascot': ['Mascot A', 'Mascot B', 'Mascot C']
    })

    assert teams_df.equals(expected_df)

def test_build_games():
    df = pd.DataFrame({
        'id': 1, 
        'year': [2000], 
        'week': 6, 
        'postseason': 1,
        'id_home_team': 1, 
        'id_away_team': 3, 
        'points_home': 4, 
        'points_away': 5,
        'completed': 1, 
        'conference_game':1, 
        'home_team_ranking': 10, 
        'away_team_ranking': 5
    })
    games_df = wr.build_games_df(df)
    expected_df = pd.DataFrame({
        'game_id': 1, 
        'year': [2000], 
        'week': 6, 
        'postseason': 1,
        'id_home_team': 1, 
        'id_away_team': 3, 
        'points_home': 4, 
        'points_away': 5,
        'completed': 1, 
        'conference_game':1, 
        'home_team_ranking': 10, 
        'away_team_ranking': 5
    })

    assert games_df.equals(expected_df)

def test_build_tables_calls_to_sql_correctly():
    # Arrange: create fake DataFrames and fake engine
    teams_df = MagicMock(name="teams_df")
    games_df = MagicMock(name="games_df")
    invalid_df = MagicMock(name="invalid_df")
    engine = MagicMock(name="engine")

    # Act
    wr.build_tables(teams_df, games_df, invalid_df, engine)

    # Assert
    teams_df.to_sql.assert_called_once_with(
        "teams",
        con=engine,
        if_exists="append",
        index=False,
    )

    games_df.to_sql.assert_called_once_with(
        "games",
        con=engine,
        if_exists="append",
        index=False,
    )

    invalid_df.to_sql.assert_called_once_with(
        "garbages",
        con=engine,
        if_exists="append",
        index=False,
    )

