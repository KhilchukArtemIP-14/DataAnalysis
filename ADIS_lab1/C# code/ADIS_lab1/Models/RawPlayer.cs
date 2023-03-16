using System;
using System.Collections.Generic;

#nullable disable

namespace ADIS_lab1.Models
{
    public partial class RawPlayer
    {
        public int PlayerId { get; set; }
        public int? MatchId { get; set; }
        public int? HeroId { get; set; }
        public int? Slot { get; set; }
        public int? Gold { get; set; }
        public int? GoldPerMin { get; set; }
        public int? XpPerMin { get; set; }
        public int? Kills { get; set; }
        public int? Deaths { get; set; }
        public int? Assists { get; set; }
        public int? LastHits { get; set; }
        public int? HeroDamage { get; set; }
        public int? HeroHeal { get; set; }
        public int? TowerDamage { get; set; }
        public int? Level { get; set; }
        public int? LeaverStatus { get; set; }
        public float? GoldHeroes { get; set; }
        public float? GoldCreeps { get; set; }
    }
}
