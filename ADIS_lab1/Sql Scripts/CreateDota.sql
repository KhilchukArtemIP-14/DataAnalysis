CREATE TABLE region_clusters_dim (
    clusterID int primary key,
    name VARCHAR(50) not null
);

CREATE TABLE hero_dim (
    heroID INT PRIMARY KEY,
    hero_name VARCHAR(50) not null,
	eff_start_date date not null,
	eff_end_date date not null,
	ref_id int foreign key references hero_dim(heroID)
);

CREATE TABLE slot_dim (
    codeID INT PRIMARY KEY,
    team VARCHAR(50) not null
);


CREATE TABLE game_mode_dim (
    modeID INT PRIMARY KEY,
    name VARCHAR(50) not null
);


CREATE TABLE start_date_dim (
    relative_date_in_seconds INT PRIMARY KEY,
    absolute_date_time DATETIME not null,
	date date not null,
	day_of_month int not null,
    time TIME not null,
	hours int not null,
	minutes int not null
);

CREATE TABLE match_fact (
    matchID INT PRIMARY KEY IDENTITY(0,1),
    clusterID INT REFERENCES region_clusters_dim(clusterID) not null,
	start_dateID INT REFERENCES start_date_dim(relative_date_in_seconds) not null,
    game_modeID INT REFERENCES game_mode_dim(modeID) not null,
    radiant_win BIT not null,
    dur_in_seconds INT not null,
    dur_in_full_mins INT not null
);

CREATE TABLE player_fact (
    playerID INT PRIMARY KEY IDENTITY(1,1) ,
    matchID INT REFERENCES match_fact(matchID) not null,
    heroID INT REFERENCES hero_dim(heroID) not null,
    slotID INT REFERENCES slot_dim(codeID) not null,
    total_gold INT not null,
    gold_per_min INT not null,
    xp_per_min INT not null,
    kills INT not null,
    deaths INT not null,
    assists INT not null,
    last_hits INT not null,
    hero_damage INT not null,
    hero_heal INT not null,
    tower_damage INT not null,
    level INT not null,
    did_quit BIT not null,
    gold_heroes REAL not null,
    gold_creeps REAL not null
);
