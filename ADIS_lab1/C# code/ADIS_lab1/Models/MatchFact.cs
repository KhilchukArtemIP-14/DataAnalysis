using System;
using System.Collections.Generic;

#nullable disable

namespace ADIS_lab1.Models
{
    public partial class MatchFact
    {
        public MatchFact()
        {
            PlayerFacts = new HashSet<PlayerFact>();
        }

        public int MatchId { get; set; }
        public int ClusterId { get; set; }
        public int StartDateId { get; set; }
        public int GameModeId { get; set; }
        public bool RadiantWin { get; set; }
        public int DurInSeconds { get; set; }
        public int DurInFullMins { get; set; }

        public virtual RegionClustersDim Cluster { get; set; }
        public virtual GameModeDim GameMode { get; set; }
        public virtual StartDateDim StartDate { get; set; }
        public virtual ICollection<PlayerFact> PlayerFacts { get; set; }
    }
}
