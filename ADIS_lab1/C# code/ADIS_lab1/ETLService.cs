using System;
using Microsoft.EntityFrameworkCore.SqlServer;
using ADIS_lab1.Models;
using Microsoft.VisualBasic.FileIO;
using System.Globalization;
using System.Linq;
namespace ADIS_lab1
{
    class ETLService
    {
        private DotaMatchesContext _context;
        public ETLService(DotaMatchesContext context)
        {
            _context = context;
        }
        public void InitialLoad()
        {
               //heroes
               using (TextFieldParser parser = new TextFieldParser(@"D:\KPI_2_2\АДІС\Lab1\Dota\hero_names.csv"))
               {
                   parser.TextFieldType = FieldType.Delimited;
                   parser.SetDelimiters(",");
                   parser.ReadFields();
                   while (!parser.EndOfData)
                   {
                       string[] fields = parser.ReadFields();
                       var tempHero = new RawHero();
                       tempHero.HeroId = Convert.ToInt32(fields[1]);
                       tempHero.HeroName = fields[2];
                       _context.RawHeroes.Add(tempHero);
                       _context.SaveChanges();
                   }
               }
               //clusters
               using (TextFieldParser parser = new TextFieldParser(@"D:\KPI_2_2\АДІС\Lab1\Dota\cluster_regions.csv"))
               {
                   parser.TextFieldType = FieldType.Delimited;
                   parser.SetDelimiters(",");
                   parser.ReadFields();
                   while (!parser.EndOfData)
                   {
                       string[] fields = parser.ReadFields();
                       var temp = new RawRegionCluster();
                       temp.ClusterId = Convert.ToInt32(fields[0]);
                       temp.ClusterName = fields[1];
                       _context.RawRegionClusters.Add(temp);
                       _context.SaveChanges();
                   }
               }

               //matches
               using (TextFieldParser parser = new TextFieldParser(@"D:\KPI_2_2\АДІС\Lab1\Dota\match.csv"))
               {
                   parser.TextFieldType = FieldType.Delimited;
                   parser.SetDelimiters(",");
                   parser.ReadFields();
                   while (!parser.EndOfData)
                   {
                       string[] fields = parser.ReadFields();
                       var temp = new RawMatch();
                       temp.MatchId = Convert.ToInt32(fields[0]);
                       temp.StartTime = Convert.ToInt32(fields[1]);
                       temp.Duration= Convert.ToInt32(fields[2]);
                       temp.GameMode= Convert.ToInt32(fields[8]);
                       temp.RadiantWin = Convert.ToBoolean(fields[9]);
                       temp.Cluster = Convert.ToInt32(fields[12]);
                       _context.RawMatches.Add(temp);
                       _context.SaveChanges();
                   }
               }

               //players
               using (TextFieldParser parser = new TextFieldParser(@"D:\KPI_2_2\АДІС\Lab1\Dota\players.csv"))
               {
                   parser.TextFieldType = FieldType.Delimited;
                   parser.SetDelimiters(",");
                   parser.ReadFields();
                   int id = 0;
                   CultureInfo culture = CultureInfo.InvariantCulture;
                   while (!parser.EndOfData)
                   {
                       string[] fields = parser.ReadFields();
                       var temp = new RawPlayer();
                       
                       temp.PlayerId = id;
                       id++;

                       temp.MatchId = Convert.ToInt32(fields[0]);
                       temp.HeroId = Convert.ToInt32(fields[2]);
                       temp.Slot = Convert.ToInt32(fields[3]);
                       temp.Gold = Convert.ToInt32(fields[4]);
                       temp.GoldPerMin = Convert.ToInt32(fields[6]);
                       temp.XpPerMin = Convert.ToInt32(fields[7]);
                       temp.Kills= Convert.ToInt32(fields[8]);
                       temp.Deaths = Convert.ToInt32(fields[9]);
                       temp.Assists = Convert.ToInt32(fields[10]);
                       temp.LastHits = Convert.ToInt32(fields[12]);
                       temp.HeroDamage= Convert.ToInt32(fields[14]);
                       temp.HeroHeal = Convert.ToInt32(fields[15]);
                       temp.TowerDamage = Convert.ToInt32(fields[16]);
                       temp.Level= Convert.ToInt32(fields[23]);
                       temp.LeaverStatus = Convert.ToInt32(fields[24]);
                       if (fields[35] != "")
                       {
                           temp.GoldHeroes = (float)Convert.ToDecimal(fields[35], culture);
                       }
                       else temp.GoldHeroes = 4950f;
                       if (fields[36] != "")
                       {
                           temp.GoldCreeps = (float)Convert.ToDecimal(fields[36], culture);
                       }
                       else temp.GoldHeroes = 5100f;
                       _context.RawPlayers.Add(temp);
                       _context.SaveChanges();
                   }
               }
        }

        public void AppendRawRegion(RawRegionCluster cluster)
        {
            cluster.ClusterId = _context.RawRegionClusters.Max(c => c.ClusterId) + 1;
            _context.RawRegionClusters.Add(cluster);
            _context.SaveChanges();
        }

        public void AppendRawPlayer(RawPlayer player)
        {
            player.PlayerId = _context.RawPlayers.Max(p => p.PlayerId) + 1;
            _context.RawPlayers.Add(player);
            _context.SaveChanges();
        }

        public void AppendRawMatch(RawMatch match)
        {
            match.MatchId = _context.RawMatches.Max(g => g.MatchId) + 1;
            _context.RawMatches.Add(match);
            _context.SaveChanges();
        }

        public void AppendRawHero(RawHero hero)
        {
            hero.HeroId = _context.RawHeroes.Max(h=> h.HeroId)+1;
            _context.RawHeroes.Add(hero);
            _context.SaveChanges();
        }

        public void AppendGameMode(GameModeDim mode)
        {
            mode.ModeId = _context.GameModeDims.Max(m => m.ModeId)+1;
            _context.GameModeDims.Add(mode);
            _context.SaveChanges();
        }
    }
}
