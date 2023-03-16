use DotaMatches

---heroes dimensions
insert into [dbo].[hero_dim](heroID,hero_name, eff_start_date,eff_end_date,ref_id) 
select heroID ,hero_name,'01/01/1970','01/01/3000', null from [dbo].[raw_heroes]
where raw_heroes.heroID not in (select heroID from [dbo].[hero_dim])


---clusters dimensions
insert into [dbo].[region_clusters_dim](clusterID,name)
select clusterID,cluster_name from [dbo].[raw_region_cluster]
where raw_region_cluster.clusterID not in (select clusterID from [region_clusters_dim])

---slots dimension
insert into [dbo].[slot_dim](codeID,team)
select distinct(slot) as code ,  case when slot>100 then 'Dire' else 'Radiant' end 
from raw_player 
where slot not in (select codeID from slot_dim)
order by code


---start dates dim
insert into [dbo].[start_date_dim](relative_date_in_seconds,absolute_date_time,date,day_of_month,time,hours,minutes)
select table1.start_time,table1.absolute_date, CAST(table1.absolute_date as date) as [date], DAY(table1.absolute_date),CAST(table1.absolute_date as time) as [time],DATEPART(HOUR, table1.absolute_date), DATEPART(MINUTE, table1.absolute_date)
from (
	select distinct(start_time) as start_time, DATEADD(ss,start_time,'1970-01-01 00:00:00') as absolute_date from raw_match
	where start_time not in (select relative_date_in_seconds from start_date_dim)
	) as table1
order by start_time



---decipher game modes
if(select count(*) from game_mode_dim)=0
begin
insert into game_mode_dim(modeID,name)
values 
(0,'None'),
(1,'All Pick'),
(2,'Captains Mode'),
(3,'Random Draft'),
(4,'Single Draft'),
(5,'All Random'),
(6, 'Intro'),
(7,'Diretide'),
(8,'Reverse Captains Mode'),
(9,'The greeviling'),
(10,'Tutorial'),
(11,'Mid Only'),
(12,'Least Played'),
(13,'New Player Pool'),
(14, 'Compendium MatchMaking'),
(15, 'Co-op vs Bots'),
(16, 'Captains Draft'),
(18,'Ability Draft'),
(20,'All Random Deathmatch'),
(21, '1v1 Mid Only'),
(22,'Ranked Matchmaking'),
(23,'Turbo Mode')
end

---matches
insert into [dbo].[match_fact](clusterID,start_dateID,game_modeID,radiant_win,dur_in_seconds,dur_in_full_mins)
(select cluster,start_time,game_mode,radiant_win,duration,duration/60
from raw_match
where raw_match.matchID not in (select match_fact.matchID from match_fact)
)

--players
insert into player_fact(matchID,heroID,slotID,total_gold,gold_per_min,xp_per_min,kills,deaths,assists,last_hits,hero_damage,hero_heal,tower_damage,level,did_quit,gold_heroes,gold_creeps)
(select matchID,heroID,slot,gold,gold_per_min,xp_per_min,kills,deaths,assists,last_hits,hero_damage,hero_heal,tower_damage,level, case when leaver_status=0 then 0 else 1 end,gold_heroes, case when gold_creeps is null then 0 else gold_creeps end
from raw_player where raw_player.playerID not in (select player_fact.playerID from player_fact) and heroID<>0
)
