-- Check all time record for a team
SELECT team_id, SUM(wins) as wins, SUM(ties) as ties, SUM(loses) as loses
FROM yearly_team
WHERE team_id = 245
GROUP BY team_id;

-- Check team_id for a specific school
SELECT team_id, school_name, mascot
FROM teams
WHERE school_name LIKE 'Texas%';

-- Overall correlation between home team and win pct
-- Moderate positive correlation (.263)
WITH team_games AS (
    SELECT
        id_home_team AS team_id,
        1 AS is_home,
        CASE WHEN points_home > points_away THEN 1 ELSE 0 END AS won
    FROM games

    UNION ALL

    SELECT
        id_away_team AS team_id,
        0 AS is_home,
        CASE WHEN points_away > points_home THEN 1 ELSE 0 END AS won
    FROM games
)
SELECT corr(is_home, won) AS correlation_home_advantage
FROM team_games;


-- Home team advantage search
WITH home AS (
    SELECT
        id_home_team AS team_id,
        COUNT(*) AS home_games,
        SUM(CASE WHEN points_home > points_away THEN 1 ELSE 0 END) AS home_wins,
        SUM(CASE WHEN points_home < points_away THEN 1 ELSE 0 END) AS home_losses
    FROM games
    GROUP BY id_home_team
),
away AS (
    SELECT
        id_away_team AS team_id,
        COUNT(*) AS away_games,
        SUM(CASE WHEN points_away > points_home THEN 1 ELSE 0 END) AS away_wins,
        SUM(CASE WHEN points_away < points_home THEN 1 ELSE 0 END) AS away_losses
    FROM games
    GROUP BY id_away_team
),
combined AS (
    SELECT
        COALESCE(h.team_id, a.team_id) AS team_id,

        -- home stats
        COALESCE(home_games, 0)  AS home_games,
        COALESCE(home_wins, 0)   AS home_wins,
        COALESCE(home_losses, 0) AS home_losses,
        CASE WHEN home_games > 0
             THEN home_wins::numeric / home_games
             ELSE NULL
        END AS home_win_pct,

        -- away stats
        COALESCE(away_games, 0)  AS away_games,
        COALESCE(away_wins, 0)   AS away_wins,
        COALESCE(away_losses, 0) AS away_losses,
        CASE WHEN away_games > 0
             THEN away_wins::numeric / away_games
             ELSE NULL
        END AS away_win_pct
    FROM home h
    FULL OUTER JOIN away a ON h.team_id = a.team_id
)
SELECT
    c.team_id,
    t.full_name,
    home_games,
    ROUND(home_win_pct, 3) AS home_win_pct,
    away_games,
    ROUND(away_win_pct, 3) AS away_win_pct,
    ROUND(home_win_pct - away_win_pct, 3) AS win_pct_diff
FROM combined c
JOIN teams t ON c.team_id = t.team_id
WHERE t.full_name IN (
    'Alabama Crimson Tide',
    'Oklahoma Sooners',
    'Ohio State Buckeyes',
    'Nebraska Cornhuskers',
    'Southern California Trojans',
    'Michigan Wolverines',
    'Notre Dame Fighting Irish',
    'Texas Longhorns',
    'Florida State Seminoles',
    'Miami Hurricanes'
)
ORDER BY win_pct_diff DESC;

-- Check all games played between two teams based on team_id
SELECT
    COUNT(*) AS total_games,
    SUM(CASE WHEN id_home_team = 245 AND points_home > points_away THEN 1
             WHEN id_away_team = 245 AND points_away > points_home THEN 1
             ELSE 0 END) AS team_245_wins,
    SUM(CASE WHEN id_home_team = 251 AND points_home > points_away THEN 1
             WHEN id_away_team = 251 AND points_away > points_home THEN 1
             ELSE 0 END) AS team_251_wins,
    SUM(CASE WHEN points_home = points_away THEN 1 ELSE 0 END) AS ties
FROM games
WHERE (id_home_team = 245 AND id_away_team = 251)
   OR (id_home_team = 251 AND id_away_team = 245);