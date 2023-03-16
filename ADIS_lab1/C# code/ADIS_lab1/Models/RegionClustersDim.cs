using System;
using System.Collections.Generic;

#nullable disable

namespace ADIS_lab1.Models
{
    public partial class RegionClustersDim
    {
        public RegionClustersDim()
        {
            MatchFacts = new HashSet<MatchFact>();
        }

        public int ClusterId { get; set; }
        public string Name { get; set; }

        public virtual ICollection<MatchFact> MatchFacts { get; set; }
    }
}
