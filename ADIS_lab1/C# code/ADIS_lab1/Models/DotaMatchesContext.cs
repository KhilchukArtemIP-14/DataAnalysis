using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

#nullable disable

namespace ADIS_lab1.Models
{
    public partial class DotaMatchesContext : DbContext
    {
        public DotaMatchesContext()
        {
        }

        public DotaMatchesContext(DbContextOptions<DotaMatchesContext> options)
            : base(options)
        {
        }

        public virtual DbSet<GameModeDim> GameModeDims { get; set; }
        public virtual DbSet<HeroDim> HeroDims { get; set; }
        public virtual DbSet<MatchFact> MatchFacts { get; set; }
        public virtual DbSet<PlayerFact> PlayerFacts { get; set; }
        public virtual DbSet<RawHero> RawHeroes { get; set; }
        public virtual DbSet<RawMatch> RawMatches { get; set; }
        public virtual DbSet<RawPlayer> RawPlayers { get; set; }
        public virtual DbSet<RawRegionCluster> RawRegionClusters { get; set; }
        public virtual DbSet<RegionClustersDim> RegionClustersDims { get; set; }
        public virtual DbSet<SlotDim> SlotDims { get; set; }
        public virtual DbSet<StartDateDim> StartDateDims { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseSqlServer("Data Source=ARTEM-PC;Initial Catalog=DotaMatches;Integrated Security=True");
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<GameModeDim>(entity =>
            {
                entity.HasKey(e => e.ModeId)
                    .HasName("PK__game_mod__68A26F7EBADD36AF");

                entity.ToTable("game_mode_dim");

                entity.Property(e => e.ModeId)
                    .ValueGeneratedNever()
                    .HasColumnName("modeID");

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasMaxLength(50)
                    .IsUnicode(false)
                    .HasColumnName("name");
            });

            modelBuilder.Entity<HeroDim>(entity =>
            {
                entity.HasKey(e => e.HeroId)
                    .HasName("PK__hero_dim__DD0E44F9719341B8");

                entity.ToTable("hero_dim");

                entity.Property(e => e.HeroId)
                    .ValueGeneratedNever()
                    .HasColumnName("heroID");

                entity.Property(e => e.EffEndDate)
                    .HasColumnType("date")
                    .HasColumnName("eff_end_date");

                entity.Property(e => e.EffStartDate)
                    .HasColumnType("date")
                    .HasColumnName("eff_start_date");

                entity.Property(e => e.HeroName)
                    .IsRequired()
                    .HasMaxLength(50)
                    .IsUnicode(false)
                    .HasColumnName("hero_name");

                entity.Property(e => e.RefId).HasColumnName("ref_id");

                entity.HasOne(d => d.Ref)
                    .WithMany(p => p.InverseRef)
                    .HasForeignKey(d => d.RefId)
                    .HasConstraintName("FK__hero_dim__ref_id__4B622666");
            });

            modelBuilder.Entity<MatchFact>(entity =>
            {
                entity.HasKey(e => e.MatchId)
                    .HasName("PK__match_fa__02C72A2D8ACF5371");

                entity.ToTable("match_fact");

                entity.Property(e => e.MatchId).HasColumnName("matchID");

                entity.Property(e => e.ClusterId).HasColumnName("clusterID");

                entity.Property(e => e.DurInFullMins).HasColumnName("dur_in_full_mins");

                entity.Property(e => e.DurInSeconds).HasColumnName("dur_in_seconds");

                entity.Property(e => e.GameModeId).HasColumnName("game_modeID");

                entity.Property(e => e.RadiantWin).HasColumnName("radiant_win");

                entity.Property(e => e.StartDateId).HasColumnName("start_dateID");

                entity.HasOne(d => d.Cluster)
                    .WithMany(p => p.MatchFacts)
                    .HasForeignKey(d => d.ClusterId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__match_fac__clust__53F76C67");

                entity.HasOne(d => d.GameMode)
                    .WithMany(p => p.MatchFacts)
                    .HasForeignKey(d => d.GameModeId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__match_fac__game___55DFB4D9");

                entity.HasOne(d => d.StartDate)
                    .WithMany(p => p.MatchFacts)
                    .HasForeignKey(d => d.StartDateId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__match_fac__start__54EB90A0");
            });

            modelBuilder.Entity<PlayerFact>(entity =>
            {
                entity.HasKey(e => e.PlayerId)
                    .HasName("PK__player_f__2CDA01D187BB8F69");

                entity.ToTable("player_fact");

                entity.Property(e => e.PlayerId).HasColumnName("playerID");

                entity.Property(e => e.Assists).HasColumnName("assists");

                entity.Property(e => e.Deaths).HasColumnName("deaths");

                entity.Property(e => e.DidQuit).HasColumnName("did_quit");

                entity.Property(e => e.GoldCreeps).HasColumnName("gold_creeps");

                entity.Property(e => e.GoldHeroes).HasColumnName("gold_heroes");

                entity.Property(e => e.GoldPerMin).HasColumnName("gold_per_min");

                entity.Property(e => e.HeroDamage).HasColumnName("hero_damage");

                entity.Property(e => e.HeroHeal).HasColumnName("hero_heal");

                entity.Property(e => e.HeroId).HasColumnName("heroID");

                entity.Property(e => e.Kills).HasColumnName("kills");

                entity.Property(e => e.LastHits).HasColumnName("last_hits");

                entity.Property(e => e.Level).HasColumnName("level");

                entity.Property(e => e.MatchId).HasColumnName("matchID");

                entity.Property(e => e.SlotId).HasColumnName("slotID");

                entity.Property(e => e.TotalGold).HasColumnName("total_gold");

                entity.Property(e => e.TowerDamage).HasColumnName("tower_damage");

                entity.Property(e => e.XpPerMin).HasColumnName("xp_per_min");

                entity.HasOne(d => d.Hero)
                    .WithMany(p => p.PlayerFacts)
                    .HasForeignKey(d => d.HeroId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__player_fa__heroI__59B045BD");

                entity.HasOne(d => d.Match)
                    .WithMany(p => p.PlayerFacts)
                    .HasForeignKey(d => d.MatchId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__player_fa__match__58BC2184");

                entity.HasOne(d => d.Slot)
                    .WithMany(p => p.PlayerFacts)
                    .HasForeignKey(d => d.SlotId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__player_fa__slotI__5AA469F6");
            });

            modelBuilder.Entity<RawHero>(entity =>
            {
                entity.HasKey(e => e.HeroId)
                    .HasName("PK__raw_hero__DD0E44F9CB8405A9");

                entity.ToTable("raw_heroes");

                entity.Property(e => e.HeroId)
                    .ValueGeneratedNever()
                    .HasColumnName("heroID");

                entity.Property(e => e.HeroName)
                    .HasMaxLength(50)
                    .IsUnicode(false)
                    .HasColumnName("hero_name");
            });

            modelBuilder.Entity<RawMatch>(entity =>
            {
                entity.HasKey(e => e.MatchId)
                    .HasName("PK__raw_matc__02C72A2DA4C98BAB");

                entity.ToTable("raw_match");

                entity.Property(e => e.MatchId)
                    .ValueGeneratedNever()
                    .HasColumnName("matchID");

                entity.Property(e => e.Cluster).HasColumnName("cluster");

                entity.Property(e => e.Duration).HasColumnName("duration");

                entity.Property(e => e.GameMode).HasColumnName("game_mode");

                entity.Property(e => e.RadiantWin).HasColumnName("radiant_win");

                entity.Property(e => e.StartTime).HasColumnName("start_time");
            });

            modelBuilder.Entity<RawPlayer>(entity =>
            {
                entity.HasKey(e => e.PlayerId)
                    .HasName("PK__raw_play__3213E83F67A2BE8C");

                entity.ToTable("raw_player");

                entity.Property(e => e.PlayerId)
                    .ValueGeneratedNever()
                    .HasColumnName("playerID");

                entity.Property(e => e.Assists).HasColumnName("assists");

                entity.Property(e => e.Deaths).HasColumnName("deaths");

                entity.Property(e => e.Gold).HasColumnName("gold");

                entity.Property(e => e.GoldCreeps).HasColumnName("gold_creeps");

                entity.Property(e => e.GoldHeroes).HasColumnName("gold_heroes");

                entity.Property(e => e.GoldPerMin).HasColumnName("gold_per_min");

                entity.Property(e => e.HeroDamage).HasColumnName("hero_damage");

                entity.Property(e => e.HeroHeal).HasColumnName("hero_heal");

                entity.Property(e => e.HeroId).HasColumnName("heroID");

                entity.Property(e => e.Kills).HasColumnName("kills");

                entity.Property(e => e.LastHits).HasColumnName("last_hits");

                entity.Property(e => e.LeaverStatus).HasColumnName("leaver_status");

                entity.Property(e => e.Level).HasColumnName("level");

                entity.Property(e => e.MatchId).HasColumnName("matchID");

                entity.Property(e => e.Slot).HasColumnName("slot");

                entity.Property(e => e.TowerDamage).HasColumnName("tower_damage");

                entity.Property(e => e.XpPerMin).HasColumnName("xp_per_min");
            });

            modelBuilder.Entity<RawRegionCluster>(entity =>
            {
                entity.HasKey(e => e.ClusterId)
                    .HasName("PK__raw_regi__07D783DD2841F2FB");

                entity.ToTable("raw_region_cluster");

                entity.Property(e => e.ClusterId)
                    .ValueGeneratedNever()
                    .HasColumnName("clusterID");

                entity.Property(e => e.ClusterName)
                    .HasMaxLength(50)
                    .IsUnicode(false)
                    .HasColumnName("cluster_name");
            });

            modelBuilder.Entity<RegionClustersDim>(entity =>
            {
                entity.HasKey(e => e.ClusterId)
                    .HasName("PK__region_c__07D783DD9CC82900");

                entity.ToTable("region_clusters_dim");

                entity.Property(e => e.ClusterId)
                    .ValueGeneratedNever()
                    .HasColumnName("clusterID");

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasMaxLength(50)
                    .IsUnicode(false)
                    .HasColumnName("name");
            });

            modelBuilder.Entity<SlotDim>(entity =>
            {
                entity.HasKey(e => e.CodeId)
                    .HasName("PK__slot_dim__47F8CFC4DFFE9A47");

                entity.ToTable("slot_dim");

                entity.Property(e => e.CodeId)
                    .ValueGeneratedNever()
                    .HasColumnName("codeID");

                entity.Property(e => e.Team)
                    .IsRequired()
                    .HasMaxLength(50)
                    .IsUnicode(false)
                    .HasColumnName("team");
            });

            modelBuilder.Entity<StartDateDim>(entity =>
            {
                entity.HasKey(e => e.RelativeDateInSeconds)
                    .HasName("PK__start_da__7275BA47EFC35E9E");

                entity.ToTable("start_date_dim");

                entity.Property(e => e.RelativeDateInSeconds)
                    .ValueGeneratedNever()
                    .HasColumnName("relative_date_in_seconds");

                entity.Property(e => e.AbsoluteDateTime)
                    .HasColumnType("datetime")
                    .HasColumnName("absolute_date_time");

                entity.Property(e => e.Date)
                    .HasColumnType("date")
                    .HasColumnName("date");

                entity.Property(e => e.DayOfMonth).HasColumnName("day_of_month");

                entity.Property(e => e.Hours).HasColumnName("hours");

                entity.Property(e => e.Minutes).HasColumnName("minutes");

                entity.Property(e => e.Time).HasColumnName("time");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}
