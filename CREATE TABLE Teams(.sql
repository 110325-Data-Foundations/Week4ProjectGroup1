CREATE TABLE Teams(
    team_id int primary key,
    full_name varchar(100),
    school_name varchar(100) not null,
    mascot varchar(100)
);

CREATE TABLE Games (
    game_id int primary key,
    year smallint,
    week smallint, 
    postseason smallint default 0 not null,
    id_home_team int not null,
    id_away_team int not null,
    points_home smallint,
    points_away smallint,
    completed smallint not null,
    conference_game smallint default 0 not null,
    home_team_ranking smallint,
    away_team_ranking smallint,

    constraint fk_home_team
        foreign key (id_home_team)
        references Teams(team_id),

    constraint fk_away_team
        foreign key (id_away_team)
        references Teams(team_id)
);

Select * from garbages limit 10
