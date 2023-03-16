using System;
using System.Collections.Generic;

#nullable disable

namespace ADIS_lab1.Models
{
    public partial class RawMatch
    {
        public int MatchId { get; set; }
        public int? StartTime { get; set; }
        public int? Duration { get; set; }
        public int? GameMode { get; set; }
        public bool? RadiantWin { get; set; }
        public int? Cluster { get; set; }
    }
}
