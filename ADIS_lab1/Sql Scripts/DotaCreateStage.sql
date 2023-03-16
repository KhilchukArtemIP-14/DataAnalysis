CREATE TABLE raw_region_cluster (
  cluster_name varchar(50),
  clusterID int PRIMARY KEY,
);

CREATE TABLE raw_heroes (
  heroID int PRIMARY KEY,
  hero_name varchar(50)
);

CREATE TABLE raw_match (
  matchID int PRIMARY KEY,
  start_time int,
  duration int,
  game_mode int ,
  radiant_win bit,
  cluster int
);

CREATE TABLE raw_player (
  playerID int PRIMARY KEY,
  matchID int,
  heroID int,
  slot int,
  gold int,
  gold_per_min int,
  xp_per_min int,
  kills int,
  deaths int,
  assists int,
  last_hits int,
  hero_damage int,
  hero_heal int,
  tower_damage int,
  level int,
  leaver_status int,
  gold_heroes REAL,
  gold_creeps REAL
);
